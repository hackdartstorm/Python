"""Program: Build Weather Data Fetcher (Issue #1465).

Difficulty: Intermediate
Category: Intermediate track

Task: Build a weather data fetcher program.

Given a city name, look the city up by name, then fetch its current conditions
and a short daily forecast. Parsed responses are returned as plain dictionaries
so the caller can read the values without touching any library object.

Input: a city name (e.g. ``"Berlin"``), optionally a number of forecast days
Expected Output: a nested ``dict`` describing the city, its current weather and
    its daily forecast

Example:
    >>> weather = fetch_weather("Berlin")           # doctest: +SKIP
    >>> weather["city"]                              # doctest: +SKIP
    'Berlin'
    >>> weather["current"]["temperature"]            # doctest: +SKIP
    23.8

Data sources
------------
Both endpoints are from Open-Meteo, which is free and needs **no API key**:

* Geocoding: ``https://geocoding-api.open-meteo.com/v1/search``
* Forecast:  ``https://api.open-meteo.com/v1/forecast``

Only the standard library is used (``urllib.request``), so this module runs
without installing anything extra. Every network call funnels through the
single private helper :func:`_http_get_json`, which keeps the parsing logic
testable offline -- the test suite below never touches the network.

Error handling
--------------
All failures raise a subclass of :class:`WeatherError`, so callers can catch one
type:

* :class:`CityNotFoundError` -- the city is unknown, or the request was malformed.
* :class:`WeatherServiceError` -- the network failed, timed out, returned a
  non-200 status, or sent back something that is not the expected JSON shape.

Usage:
    python build_weather_data_fetcher.py Berlin
    python build_weather_data_fetcher.py "New York" --days 3 --units fahrenheit
"""

from __future__ import annotations

import argparse
import json
import sys
from email.message import Message
from typing import TYPE_CHECKING, Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

if TYPE_CHECKING:
    # 	yping.Self needs 3.11+, but annotations are strings under
    # rom __future__ import annotations, so this import is never evaluated at
    # runtime and the module still imports on 3.10.
    from typing import Self

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

#: Every network call gives up after this many seconds so a hung server cannot
#: freeze the program forever.
DEFAULT_TIMEOUT = 10.0

#: Open-Meteo caps ``forecast_days`` at 16.
MAX_FORECAST_DAYS = 16

#: WMO weather interpretation codes, as published by the World Meteorological
#: Organization. The API returns the numeric code, which is meaningless to a
#: human reader, so it is translated into a short description.
WMO_WEATHER_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


class WeatherError(Exception):
    """Base class for every error raised by this module."""


class CityNotFoundError(WeatherError):
    """Raised when the supplied city name cannot be resolved to a location."""


class WeatherServiceError(WeatherError):
    """Raised when the upstream service cannot be reached or returns garbage."""


def describe_weather_code(code: Any) -> str:
    """Translate a WMO weather code into a human-readable condition.

    Args:
        code: The numeric code reported by Open-Meteo. Anything that is not a
            known integer falls back to a generic description rather than
            raising, because an unknown future code should not break a fetch.

    Returns:
        A short description such as ``"Clear sky"``.

    Example:
        >>> describe_weather_code(0)
        'Clear sky'
        >>> describe_weather_code(999)
        'Unknown conditions'
    """
    if isinstance(code, bool) or not isinstance(code, int):
        return "Unknown conditions"
    return WMO_WEATHER_CODES.get(code, "Unknown conditions")


def _http_get_json(
    url: str, params: dict[str, Any], timeout: float = DEFAULT_TIMEOUT
) -> dict[str, Any]:
    """Perform a GET request and decode the JSON body.

    This is the only place in the module that touches the network. Keeping it
    isolated means the parsing code can be tested by replacing this one
    function, with no real HTTP traffic.

    Args:
        url: The endpoint to call.
        params: Query-string parameters to append to the URL.
        timeout: Seconds to wait before giving up.

    Returns:
        The decoded JSON body, which must be a JSON object.

    Raises:
        WeatherServiceError: On a network failure, a timeout, a non-200 status,
            a body that is not valid JSON, or a body that is not an object.
    """
    full_url = f"{url}?{urlencode(params)}"
    try:
        # `timeout` is passed to the socket layer, so a stalled server raises
        # instead of hanging forever.
        with urlopen(full_url, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise WeatherServiceError(f"{url} returned HTTP {status}")
            raw_bytes = response.read()
    except HTTPError as exc:
        # A 4xx/5xx status; the body often explains why.
        raise WeatherServiceError(f"{url} returned HTTP {exc.code}") from exc
    except TimeoutError as exc:
        raise WeatherServiceError(f"Request to {url} timed out") from exc
    except URLError as exc:
        # Wraps connection-refused, DNS failure and, on some platforms, timeout.
        raise WeatherServiceError(f"Could not reach {url}: {exc.reason}") from exc
    except OSError as exc:
        raise WeatherServiceError(f"Could not reach {url}: {exc}") from exc

    try:
        payload = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WeatherServiceError(f"{url} did not return valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise WeatherServiceError(
            f"{url} returned {type(payload).__name__}, expected a JSON object"
        )
    return payload


def _validate_city(city: Any) -> str:
    """Check that ``city`` is a usable city name and return it stripped.

    Args:
        city: The candidate city name.

    Returns:
        The trimmed city name.

    Raises:
        CityNotFoundError: If the name is empty, blank, or not a string.

    Example:
        >>> _validate_city("  Berlin ")
        'Berlin'
    """
    if not isinstance(city, str):
        raise CityNotFoundError(
            f"City name must be a string, got {type(city).__name__}"
        )
    cleaned = city.strip()
    if not cleaned:
        raise CityNotFoundError("City name must not be empty")
    return cleaned


def _validate_days(days: Any) -> int:
    """Check that ``days`` is an integer within the range the API accepts.

    Args:
        days: The requested number of forecast days.

    Returns:
        The validated number of days.

    Raises:
        TypeError: If ``days`` is not an ``int``. ``bool`` is rejected
            explicitly because ``True`` would otherwise count as 1.
        ValueError: If ``days`` is outside the supported 1-16 range.

    Example:
        >>> _validate_days(3)
        3
    """
    if isinstance(days, bool) or not isinstance(days, int):
        raise TypeError(f"days must be an int, got {type(days).__name__}")
    if not 1 <= days <= MAX_FORECAST_DAYS:
        raise ValueError(f"days must be between 1 and {MAX_FORECAST_DAYS}")
    return days


def _validate_units(units: Any) -> str:
    """Normalise the unit argument to ``"celsius"`` or ``"fahrenheit"``.

    Args:
        units: The requested unit, in any capitalisation.

    Returns:
        The lower-cased unit name.

    Raises:
        TypeError: If the unit is not a string.
        ValueError: If the unit is not one of the two supported values.

    Example:
        >>> _validate_units("Fahrenheit")
        'fahrenheit'
    """
    if not isinstance(units, str):
        raise TypeError(f"units must be a string, got {type(units).__name__}")
    cleaned = units.strip().lower()
    if cleaned not in {"celsius", "fahrenheit"}:
        raise ValueError("units must be either 'celsius' or 'fahrenheit'")
    return cleaned


def geocode_city(city: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Look up a city name and return its coordinates.

    Args:
        city: Name of the city, e.g. ``"Berlin"``. Matching is case-insensitive
            on the service side.
        timeout: Seconds to wait for the response.

    Returns:
        A ``dict`` with ``name``, ``country``, ``latitude`` and ``longitude``.

    Raises:
        CityNotFoundError: If the name is unusable or the service knows no such
            place.
        WeatherServiceError: If the service is unreachable or misbehaves.
    """
    cleaned = _validate_city(city)
    payload = _http_get_json(
        GEOCODING_URL, {"name": cleaned, "count": 1, "format": "json"}, timeout
    )

    # A miss is reported as a well-formed object with an empty `results` list,
    # which is not an error at the HTTP level, so it is handled here.
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        raise CityNotFoundError(f"Unknown city: {cleaned!r}")
    first = results[0]
    if not isinstance(first, dict):
        raise WeatherServiceError("Geocoding service returned a malformed result")

    return {
        "name": first.get("name", cleaned),
        "country": first.get("country", ""),
        "latitude": first.get("latitude"),
        "longitude": first.get("longitude"),
    }


def _build_daily_entries(daily: dict[str, Any]) -> list[dict[str, Any]]:
    """Zip the parallel arrays in the ``daily`` block into a list of dicts.

    Open-Meteo returns columns (``time``, ``temperature_2m_max``, ...) rather
    than rows, so they are transposed here into one dict per day.

    Args:
        daily: The ``daily`` block of the forecast response.

    Returns:
        A list of per-day ``dict`` values.

    Raises:
        WeatherServiceError: If the columns are missing or of uneven length.
    """
    dates = daily.get("time")
    highs = daily.get("temperature_2m_max")
    lows = daily.get("temperature_2m_min")
    codes = daily.get("weather_code")

    if not isinstance(dates, list) or not dates:
        raise WeatherServiceError("Forecast response contained no daily data")
    # Missing columns are tolerated as long as the lengths agree, because the
    # API omits a column entirely when no value for it is available.
    lengths = {
        len(column)
        for column in (dates, highs, lows, codes)
        if isinstance(column, list)
    }
    if len(lengths) > 1:
        raise WeatherServiceError("Forecast response had mismatched daily columns")

    def column_at(column: Any, index: int) -> Any:
        """Return one entry of an optional column, or ``None`` if absent."""
        if isinstance(column, list) and index < len(column):
            return column[index]
        return None

    entries: list[dict[str, Any]] = []
    for index, date in enumerate(dates):
        code = column_at(codes, index)
        entries.append(
            {
                "date": date,
                "temperature_max": column_at(highs, index),
                "temperature_min": column_at(lows, index),
                "weather_code": code,
                "condition": describe_weather_code(code),
            }
        )
    return entries


def fetch_weather(
    city: str,
    days: int = 1,
    units: str = "celsius",
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Fetch the current weather and a short forecast for ``city``.

    Args:
        city: Name of the city to look up.
        days: How many forecast days to include, 1-16.
        units: ``"celsius"`` or ``"fahrenheit"``.
        timeout: Seconds to wait for each of the two HTTP calls.

    Returns:
        A nested ``dict`` with the keys ``city``, ``country``, ``latitude``,
        ``longitude``, ``timezone``, ``units``, ``current`` and ``daily``.

    Raises:
        CityNotFoundError: If the city cannot be resolved.
        WeatherServiceError: If either request fails or returns bad data.
        TypeError: If ``days`` or ``units`` have the wrong type.
        ValueError: If ``days`` or ``units`` are out of range.

    Example:
        >>> fetch_weather("Berlin")["current"]["condition"]  # doctest: +SKIP
        'Clear sky'
    """
    checked_days = _validate_days(days)
    checked_units = _validate_units(units)
    location = geocode_city(city, timeout=timeout)

    payload = _http_get_json(
        FORECAST_URL,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min",
            "forecast_days": checked_days,
            "temperature_unit": checked_units,
            "timezone": "auto",
        },
        timeout,
    )

    current = payload.get("current")
    if not isinstance(current, dict):
        raise WeatherServiceError("Forecast response contained no current weather")
    daily = payload.get("daily")
    if not isinstance(daily, dict):
        raise WeatherServiceError("Forecast response contained no daily forecast")

    code = current.get("weather_code")
    return {
        "city": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": payload.get("timezone", ""),
        "units": checked_units,
        "current": {
            "time": current.get("time"),
            "temperature": current.get("temperature_2m"),
            "apparent_temperature": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "weather_code": code,
            "condition": describe_weather_code(code),
        },
        "daily": _build_daily_entries(daily),
    }


def format_report(weather: dict[str, Any]) -> str:
    """Render a fetched-weather dict as a readable multi-line report.

    Args:
        weather: A dict in the shape returned by :func:`fetch_weather`.

    Returns:
        A human-readable report, ready to print.

    Example:
        >>> format_report({"city": "Berlin", "country": "Germany",
        ...                "current": {"temperature": 23.8,
        ...                          "condition": "Clear sky"},
        ...                "daily": [], "units": "celsius"})
        'Berlin, Germany\\n  Now: 23.8 degC, Clear sky\\n  No forecast available.'
    """
    unit_label = "degC" if weather.get("units", "celsius") == "celsius" else "degF"
    current = weather.get("current", {})
    temperature = current.get("temperature")
    condition = current.get("condition", "Unknown conditions")

    temperature_text = (
        f"{temperature} {unit_label}" if temperature is not None else "unavailable"
    )
    lines = [
        f"{weather.get('city', 'Unknown')}, {weather.get('country', '')}".strip(", ")
    ]
    lines.append(f"  Now: {temperature_text}, {condition}")

    daily = weather.get("daily") or []
    if daily:
        lines.append("  Forecast:")
        for day in daily:
            high = day.get("temperature_max")
            low = day.get("temperature_min")
            if high is None and low is None:
                lines.append(f"    {day.get('date')}: {day.get('condition')}")
            else:
                lines.append(
                    f"    {day.get('date')}: {low}-{high} {unit_label}, "
                    f"{day.get('condition')}"
                )
    else:
        lines.append("  No forecast available.")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
# Every test replaces `_http_get_json` with a stub, so the suite is fast,
# deterministic and never needs network access.

# A realistic geocoding response, trimmed to the fields this module reads.
SAMPLE_GEOCODING: dict[str, Any] = {
    "results": [
        {
            "name": "Berlin",
            "country": "Germany",
            "latitude": 52.52437,
            "longitude": 13.41053,
        }
    ]
}

# A realistic forecast response in the column layout Open-Meteo uses.
SAMPLE_FORECAST: dict[str, Any] = {
    "latitude": 52.52437,
    "longitude": 13.41053,
    "timezone": "Europe/Berlin",
    "current_units": {"temperature_2m": "°C"},
    "current": {
        "time": "2026-09-27T14:00",
        "temperature_2m": 23.8,
        "apparent_temperature": 22.9,
        "relative_humidity_2m": 44,
        "wind_speed_10m": 11.2,
        "weather_code": 0,
    },
    "daily": {
        "time": ["2026-09-27", "2026-09-28"],
        "temperature_2m_max": [24.1, 21.7],
        "temperature_2m_min": [13.2, 12.4],
        "weather_code": [0, 61],
    },
}


class _FakeTransport:
    """Stand-in for :func:`_http_get_json` that replays canned payloads.

    Attributes:
        calls: Every ``(url, params, timeout)`` triple seen, so a test can
            assert on the request that would have been sent.
    """

    def __init__(self, geocoding: Any, forecast: Any) -> None:
        self.geocoding = geocoding
        self.forecast = forecast
        self.calls: list[tuple[str, dict[str, Any], float]] = []

    def __call__(
        self, url: str, params: dict[str, Any], timeout: float = DEFAULT_TIMEOUT
    ) -> Any:
        self.calls.append((url, params, timeout))
        if url == GEOCODING_URL:
            return self.geocoding
        return self.forecast


def _run_tests() -> None:
    """Run the self-checks covering normal input, edge cases and failures."""
    original_http_get_json = globals()["_http_get_json"]

    def use_fake(geocoding: Any, forecast: Any) -> _FakeTransport:
        """Install a fake transport and return it for later assertions."""
        fake = _FakeTransport(geocoding, forecast)
        globals()["_http_get_json"] = fake
        return fake

    try:
        # --- Normal input: the documented happy path -----------------------
        fake = use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
        weather = fetch_weather("Berlin", days=2)
        assert weather["city"] == "Berlin"
        assert weather["country"] == "Germany"
        assert weather["latitude"] == 52.52437
        assert weather["timezone"] == "Europe/Berlin"
        assert weather["units"] == "celsius"
        # The parsed response is a plain dict of plain values.
        assert weather["current"]["temperature"] == 23.8
        assert weather["current"]["humidity"] == 44
        assert weather["current"]["wind_speed"] == 11.2
        assert weather["current"]["condition"] == "Clear sky"
        # Columns were transposed into one dict per day.
        assert len(weather["daily"]) == 2
        assert weather["daily"][0]["date"] == "2026-09-27"
        assert weather["daily"][0]["temperature_max"] == 24.1
        assert weather["daily"][0]["temperature_min"] == 13.2
        assert weather["daily"][1]["condition"] == "Slight rain"
        # Exactly two HTTP calls: geocode first, then forecast.
        assert len(fake.calls) == 2
        assert fake.calls[0][0] == GEOCODING_URL
        assert fake.calls[1][0] == FORECAST_URL
        # The forecast request carried the coordinates and the units.
        forecast_params = fake.calls[1][1]
        assert forecast_params["latitude"] == 52.52437
        assert forecast_params["longitude"] == 13.41053
        assert forecast_params["temperature_unit"] == "celsius"
        assert forecast_params["forecast_days"] == 2

        # --- Normal input: unit and whitespace handling ---------------------
        fake = use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
        weather = fetch_weather("  bErLiN  ", units="Fahrenheit")
        assert weather["units"] == "fahrenheit"
        assert fake.calls[1][1]["temperature_unit"] == "fahrenheit"
        # The service, not this module, is what trims and case-folds the name,
        # so the trimmed form is what gets sent.
        assert fake.calls[0][1]["name"] == "bErLiN"

        # --- Edge cases -----------------------------------------------------
        # One forecast day, the documented default.
        fake = use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
        assert len(fetch_weather("Berlin")["daily"]) == 2
        assert fake.calls[1][1]["forecast_days"] == 1

        # A city whose name the service echoes back without a country.
        fake = use_fake(
            {"results": [{"name": "Nowhere", "latitude": 1.0, "longitude": 2.0}]},
            SAMPLE_FORECAST,
        )
        assert fetch_weather("Nowhere")["country"] == ""

        # Missing optional daily columns are tolerated, not fatal.
        fake = use_fake(
            SAMPLE_GEOCODING,
            {
                "timezone": "UTC",
                "current": {"temperature_2m": 5.0},
                "daily": {"time": ["2026-09-27"]},
            },
        )
        day = fetch_weather("Berlin")["daily"][0]
        assert day["temperature_max"] is None
        assert day["condition"] == "Unknown conditions"

        # An unknown future WMO code degrades gracefully.
        assert describe_weather_code(1234) == "Unknown conditions"
        assert describe_weather_code(None) == "Unknown conditions"
        assert describe_weather_code(True) == "Unknown conditions"
        assert describe_weather_code(95) == "Thunderstorm"

        # Validation helpers.
        assert _validate_city(" Berlin ") == "Berlin"
        assert _validate_days(1) == 1
        assert _validate_days(MAX_FORECAST_DAYS) == MAX_FORECAST_DAYS
        assert _validate_units("CELSIUS") == "celsius"

        # --- Failure case 1: unknown city -----------------------------------
        use_fake({"results": []}, SAMPLE_FORECAST)
        try:
            fetch_weather("Atlantis")
        except CityNotFoundError as exc:
            assert "Atlantis" in str(exc)
        else:
            raise AssertionError("expected CityNotFoundError for an unknown city")

        # --- Failure case 2: bad input, rejected before any network call ----
        for bad_city in ("", "   ", None, 42, ["Berlin"]):
            fake = use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
            try:
                fetch_weather(bad_city)  # type: ignore[arg-type]
            except CityNotFoundError:
                assert fake.calls == [], f"{bad_city!r} must not reach the network"
            else:
                raise AssertionError(f"expected CityNotFoundError for {bad_city!r}")

        for bad_days, error_type in (
            (2.5, TypeError),
            (True, TypeError),
            ("3", TypeError),
            (None, TypeError),
            (0, ValueError),
            (-1, ValueError),
            (MAX_FORECAST_DAYS + 1, ValueError),
        ):
            fake = use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
            try:
                fetch_weather("Berlin", days=bad_days)  # type: ignore[arg-type]
            except error_type:
                assert fake.calls == [], f"days={bad_days!r} must not reach the network"
            else:
                raise AssertionError(
                    f"expected {error_type.__name__} for days={bad_days!r}"
                )

        for bad_units, error_type in (
            (5, TypeError),
            (None, TypeError),
            ("kelvin", ValueError),
            ("", ValueError),
        ):
            fake = use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
            try:
                fetch_weather("Berlin", units=bad_units)  # type: ignore[arg-type]
            except error_type:
                assert fake.calls == [], f"units={bad_units!r} must not reach network"
            else:
                raise AssertionError(
                    f"expected {error_type.__name__} for units={bad_units!r}"
                )

        # --- Failure case 3: malformed service responses ---------------------
        # A geocoding result that is not a dict.
        use_fake({"results": ["Berlin"]}, SAMPLE_FORECAST)
        try:
            fetch_weather("Berlin")
        except WeatherServiceError:
            pass
        else:
            raise AssertionError("expected WeatherServiceError for a malformed result")

        # A forecast with no `current` block.
        use_fake(SAMPLE_GEOCODING, {"daily": SAMPLE_FORECAST["daily"]})
        try:
            fetch_weather("Berlin")
        except WeatherServiceError:
            pass
        else:
            raise AssertionError("expected WeatherServiceError for missing current")

        # A forecast with no `daily` block.
        use_fake(SAMPLE_GEOCODING, {"current": SAMPLE_FORECAST["current"]})
        try:
            fetch_weather("Berlin")
        except WeatherServiceError:
            pass
        else:
            raise AssertionError("expected WeatherServiceError for missing daily")

        # An empty `daily.time`, so there is nothing to report.
        use_fake(
            SAMPLE_GEOCODING,
            {"current": SAMPLE_FORECAST["current"], "daily": {"time": []}},
        )
        try:
            fetch_weather("Berlin")
        except WeatherServiceError:
            pass
        else:
            raise AssertionError("expected WeatherServiceError for empty daily data")

        # Daily columns of uneven length.
        use_fake(
            SAMPLE_GEOCODING,
            {
                "current": SAMPLE_FORECAST["current"],
                "daily": {
                    "time": ["2026-09-27", "2026-09-28"],
                    "temperature_2m_max": [1.0],
                },
            },
        )
        try:
            fetch_weather("Berlin")
        except WeatherServiceError:
            pass
        else:
            raise AssertionError("expected WeatherServiceError for mismatched columns")

        # --- Failure case 4: transport-level problems -----------------------
        # These exercise the real `_http_get_json`, so the fake installed above
        # is removed first. `urlopen` itself is then replaced, which keeps the
        # tests deterministic and offline while still covering every branch of
        # the error handling.
        globals()["_http_get_json"] = original_http_get_json

        class _FakeResponse:
            """Minimal stand-in for the object ``urlopen`` yields."""

            status = 200

            def read(self) -> bytes:
                return b'{"ok": true}'

            def __enter__(self) -> Self:
                return self

            def __exit__(self, *args: object) -> None:
                return None

        def expect_service_error(label: str, fragment: str, replacement: Any) -> None:
            """Install ``replacement`` as urlopen and assert the error message.

            Args:
                label: Human-readable name of the case, used in failures.
                fragment: Substring the raised message must contain.
                replacement: Callable standing in for ``urlopen``.
            """
            saved = globals()["urlopen"]
            try:
                globals()["urlopen"] = replacement
                try:
                    _http_get_json("https://example.invalid", {})
                except WeatherServiceError as exc:
                    assert fragment in str(exc), f"{label}: unexpected message {exc}"
                else:
                    raise AssertionError(f"{label}: expected WeatherServiceError")
            finally:
                globals()["urlopen"] = saved

        # A JSON body that is an array rather than an object.
        class _ArrayResponse(_FakeResponse):
            def read(self) -> bytes:
                return b"[1, 2, 3]"

        expect_service_error(
            "JSON array body", "JSON object", lambda *a, **k: _ArrayResponse()
        )

        # A non-200 status is treated as a service error.
        class _NotFoundResponse(_FakeResponse):
            status = 404

        expect_service_error("HTTP 404", "404", lambda *a, **k: _NotFoundResponse())

        # A body that is not JSON at all.
        class _BadJsonResponse(_FakeResponse):
            def read(self) -> bytes:
                return b"not json at all"

        expect_service_error(
            "invalid JSON", "valid JSON", lambda *a, **k: _BadJsonResponse()
        )

        # A body that is not valid UTF-8.
        class _BadEncodingResponse(_FakeResponse):
            def read(self) -> bytes:
                return b"\xff\xfe\x00"

        expect_service_error(
            "bad encoding", "valid JSON", lambda *a, **k: _BadEncodingResponse()
        )

        # An HTTP error status raised directly by urlopen.
        def _raise_http_error(*args: Any, **kwargs: Any) -> Any:
            raise HTTPError(
                "https://example.invalid", 500, "Server Error", Message(), None
            )

        expect_service_error("HTTPError", "500", _raise_http_error)

        # A connection failure, e.g. DNS or a refused port.
        def _raise_url_error(*args: Any, **kwargs: Any) -> Any:
            raise URLError("Name or service not known")

        expect_service_error("URLError", "Could not reach", _raise_url_error)

        # A timeout. `socket.timeout` is an alias of `TimeoutError` on 3.10+.
        def _raise_timeout(*args: Any, **kwargs: Any) -> Any:
            raise TimeoutError("timed out")

        expect_service_error("timeout", "timed out", _raise_timeout)

        # A bare OS failure that is neither of the above.
        def _raise_os_error(*args: Any, **kwargs: Any) -> Any:
            raise OSError("connection reset")

        expect_service_error("OSError", "Could not reach", _raise_os_error)

        # --- Report formatting ---------------------------------------------
        # Re-seed with the good sample so this section does not depend on
        # whichever fake happened to be installed last.
        use_fake(SAMPLE_GEOCODING, SAMPLE_FORECAST)
        weather = fetch_weather("Berlin", days=2)
        report = format_report(weather)
        assert "Berlin" in report
        assert "23.8 degC" in report
        assert "Slight rain" in report
        assert "degF" in format_report(
            {"city": "Berlin", "current": {"temperature": 74.8}, "units": "fahrenheit"}
        )
        # Missing data must not crash the formatter.
        assert "unavailable" in format_report({"city": "Berlin", "current": {}})
        assert "No forecast available." in format_report({"current": {}})

    finally:
        globals()["_http_get_json"] = original_http_get_json

    print("All tests passed.")


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point.

    Args:
        argv: Argument list, defaulting to ``sys.argv[1:]``.

    Returns:
        ``0`` on success, ``1`` if the weather could not be fetched.
    """
    parser = argparse.ArgumentParser(
        description="Fetch current weather and a short forecast for a city."
    )
    parser.add_argument("city", help="City name, e.g. Berlin")
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        default=3,
        help=f"Forecast days, 1-{MAX_FORECAST_DAYS} (default: 3)",
    )
    parser.add_argument(
        "-u",
        "--units",
        default="celsius",
        choices=["celsius", "fahrenheit"],
        help="Temperature unit (default: celsius)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Network timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    args = parser.parse_args(argv)

    try:
        weather = fetch_weather(
            args.city, days=args.days, units=args.units, timeout=args.timeout
        )
    except WeatherError as exc:
        # One handler for every expected failure, so the CLI never shows a
        # traceback for a bad city name or an offline machine.
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(format_report(weather))
    return 0


if __name__ == "__main__":
    # Running the file with no arguments runs the offline self-checks, so a
    # reader can verify the parsing and error handling without a network
    # connection or an API key. Pass a city name for the real fetcher.
    if len(sys.argv) == 1 or sys.argv[1] == "--test":
        _run_tests()
        raise SystemExit(0)
    raise SystemExit(main())
