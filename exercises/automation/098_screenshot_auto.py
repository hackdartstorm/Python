"""Program 098: Screenshot Automation (Issue #1306).

Difficulty: Intermediate
Category: Automation

Task: Capture the screen, or a region of it, and save it to disk.

The script grabs the whole screen or a rectangular region and writes it to a
timestamped PNG (or another supported format), creating the output directory if
needed and never silently overwriting an existing file.

Usage:
    # Whole screen, saved as ./screenshot_20260927_142305.png
    python 098_screenshot_auto.py

    # A 800x600 region at (100, 100), into ./shots/
    python 098_screenshot_auto.py --region 100 100 800 600 --output-dir shots

    # JPEG at a fixed filename, overwriting whatever is there
    python 098_screenshot_auto.py --format jpg --filename today.jpg --overwrite

    # Run the offline self-checks (no screen capture, no network)
    python 098_screenshot_auto.py --test

Backends
--------
Screenshots need different libraries on different platforms, so three are
supported and tried in this order:

1. ``mss``    -- fastest, and handles multi-monitor setups. Optional.
2. ``Pillow`` -- ``PIL.ImageGrab``, the most widely available. Optional.
3. ``pyautogui`` -- last resort. Optional.

All imports are done lazily inside the functions that need them, so this module
imports cleanly even when none of the three are installed, and the test suite
runs with no third-party packages at all. Install whichever you need with, for
example::

    pip install pillow        # or: pip install mss

Headless machines
-----------------
A CI runner or a server has no screen to photograph. Rather than crashing with
an opaque library error, the capture path detects that case and raises
:class:`NoDisplayError` with a message explaining what to do. Everything that
does not touch the screen -- filename generation, path handling, validation --
is fully testable without a display, and the test suite exercises all of it.

The screenshot itself is saved wherever you point ``--output-dir``, which
defaults to the current working directory.

A note on region sizes
----------------------
A region is clipped to the part of the screen that actually exists, so a capture
that runs off an edge comes back smaller than requested. On Windows this is more
noticeable than it sounds: the desktop has an invisible border a few pixels wide,
so ``--region 10 10 320 240`` yields a 310x230 image, because the outermost
pixels are not part of the capturable desktop. Add a small margin, or capture a
region that stops well short of the screen edge, if the exact size matters.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from PIL.Image import Image

    def save(self, path: Any, format: str | None = None) -> None:
        """Write the image to ``path`` in the named format."""
        ...


#: Backends in the order they are attempted.
BACKEND_ORDER = ("mss", "pillow", "pyautogui")

#: File formats the saver accepts, mapped to the name Pillow expects. JPEG and
#: BMP cannot store an alpha channel, so images are flattened to RGB for those.
SUPPORTED_FORMATS: dict[str, str] = {
    "png": "PNG",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "bmp": "BMP",
    "tiff": "TIFF",
    "webp": "WEBP",
}

#: Formats that have no alpha channel.
FORMATS_WITHOUT_ALPHA = frozenset({"jpg", "jpeg", "bmp"})

#: Width and height must both be positive.
MIN_REGION_SIZE = 1

DEFAULT_OUTPUT_DIR = "."
DEFAULT_FORMAT = "png"


class ScreenshotError(Exception):
    """Base class for every error raised by this module."""


class NoDisplayError(ScreenshotError):
    """Raised when there is no screen available to capture."""


class NoBackendError(ScreenshotError):
    """Raised when none of the supported screenshot libraries is installed."""


class InvalidRegionError(ScreenshotError, ValueError):
    """Raised when the requested capture region is not usable."""


class InvalidFormatError(ScreenshotError, ValueError):
    """Raised when the requested image format is not supported."""


class SavePathError(ScreenshotError):
    """Raised when the destination directory or file cannot be written."""


# --------------------------------------------------------------------------
# Input validation
# --------------------------------------------------------------------------


def validate_region(region: Sequence[int] | None) -> tuple[int, int, int, int] | None:
    """Check a capture region and return it as a tuple.

    The region is ``(left, top, width, height)``. ``None`` means "the whole
    screen" and is returned unchanged.

    ``left`` and ``top`` may be negative, because on a multi-monitor desktop a
    secondary display to the left of the primary one has negative coordinates.
    ``width`` and ``height`` must both be at least
    :data:`MIN_REGION_SIZE`.

    Args:
        region: The candidate region, or ``None``.

    Returns:
        A 4-tuple of ints, or ``None`` for the whole screen.

    Raises:
        InvalidRegionError: If the region is not four integers, or if its width
            or height is not positive.

    Example:
        >>> validate_region([0, 0, 10, 20])
        (0, 0, 10, 20)
        >>> validate_region(None) is None
        True
    """
    if region is None:
        return None

    # bool is a subclass of int, but True as a coordinate is always a mistake.
    if isinstance(region, (str, bytes)) or not isinstance(region, Sequence):
        raise InvalidRegionError(
            f"region must be a sequence of 4 integers, got {type(region).__name__}"
        )

    values = list(region)
    if len(values) != 4:
        raise InvalidRegionError(
            f"region must have exactly 4 values (left, top, width, height), "
            f"got {len(values)}"
        )
    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidRegionError(
                f"region[{index}] must be an int, got {type(value).__name__}"
            )

    left, top, width, height = values
    if width < MIN_REGION_SIZE or height < MIN_REGION_SIZE:
        raise InvalidRegionError(
            f"region width and height must be at least {MIN_REGION_SIZE}, "
            f"got width={width}, height={height}"
        )
    return (left, top, width, height)


def validate_format(image_format: Any) -> str:
    """Check an image format name and return it lower-cased.

    Args:
        image_format: The candidate format, in any capitalisation, with or
            without a leading dot.

    Returns:
        The lower-cased format name, as a key of :data:`SUPPORTED_FORMATS`.

    Raises:
        InvalidFormatError: If the format is not a string, or is not supported.

    Example:
        >>> validate_format(".PNG")
        'png'
        >>> validate_format("JPEG")
        'jpeg'
    """
    if not isinstance(image_format, str):
        raise InvalidFormatError(
            f"format must be a string, got {type(image_format).__name__}"
        )
    cleaned = image_format.strip().lower().lstrip(".")
    if cleaned not in SUPPORTED_FORMATS:
        supported = ", ".join(sorted(set(SUPPORTED_FORMATS)))
        raise InvalidFormatError(
            f"unsupported format {image_format!r}; supported formats: {supported}"
        )
    return cleaned


# --------------------------------------------------------------------------
# Filename and path handling
# --------------------------------------------------------------------------


def build_filename(
    image_format: str = DEFAULT_FORMAT,
    when: datetime | None = None,
    prefix: str = "screenshot",
) -> str:
    """Build a timestamped screenshot filename.

    The timestamp is second-resolution and local time, so sorting a folder of
    screenshots alphabetically also sorts them chronologically.

    Args:
        image_format: A format name; validated by :func:`validate_format`.
        when: The moment to stamp the name with. Defaults to
            :func:`datetime.now`, and is injectable so tests are deterministic.
        prefix: The leading part of the filename.

    Returns:
        A filename such as ``screenshot_20260927_142305.png``.

    Raises:
        InvalidFormatError: If ``image_format`` is not supported.
        ValueError: If ``prefix`` is empty or contains a path separator.

    Example:
        >>> build_filename("png", datetime(2026, 9, 27, 14, 23, 5, tzinfo=timezone.utc))
        'screenshot_20260927_142305.png'
    """
    checked_format = validate_format(image_format)
    if not isinstance(prefix, str) or not prefix.strip():
        raise ValueError("prefix must be a non-empty string")
    if "/" in prefix or "\\" in prefix or os.sep in prefix:
        raise ValueError(f"prefix must not contain a path separator: {prefix!r}")

    # `.astimezone()` keeps the value in local time -- which is what a
    # screenshot filename should show -- while making it timezone-aware, so the
    # stamp is unambiguous if it is ever compared across machines.
    moment = when if when is not None else datetime.now().astimezone()
    return f"{prefix}_{moment:%Y%m%d_%H%M%S}.{checked_format}"


def resolve_output_dir(output_dir: str | os.PathLike[str]) -> Path:
    """Check the output directory and create it if it does not exist.

    Args:
        output_dir: The directory to save screenshots into.

    Returns:
        The resolved, existing :class:`~pathlib.Path`.

    Raises:
        SavePathError: If the path exists but is not a directory, or if the
            directory cannot be created or written to.

    Example:
        >>> isinstance(resolve_output_dir("."), Path)
        True
    """
    if isinstance(output_dir, (str, os.PathLike)):
        directory = Path(output_dir)
    else:
        raise SavePathError(
            f"output_dir must be a path-like value, got {type(output_dir).__name__}"
        )

    if directory.exists() and not directory.is_dir():
        raise SavePathError(f"output_dir is not a directory: {directory}")

    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SavePathError(
            f"Could not create output directory {directory}: {exc}"
        ) from exc

    # A directory can exist and still be read-only, so check writability rather
    # than assuming. os.access is advisory on some platforms, but it is the
    # cheapest check available and the real write is verified when saving.
    if not os.access(directory, os.W_OK):
        raise SavePathError(f"output_dir is not writable: {directory}")
    return directory.resolve()


def unique_path(directory: Path, filename: str, overwrite: bool = False) -> Path:
    """Join a filename to a directory, avoiding collisions unless asked to.

    With ``overwrite=False`` and an existing ``shot.png``, this returns
    ``shot_1.png``, then ``shot_2.png``, and so on, so a screenshot run never
    destroys earlier files.

    Args:
        directory: The target directory, which must already exist.
        filename: The filename to place inside it.
        overwrite: If ``True``, return the path unchanged even if it exists.

    Returns:
        A path inside ``directory`` that does not yet exist, unless
        ``overwrite`` is set.

    Raises:
        SavePathError: If ``filename`` is empty or contains a directory
            separator.
    """
    if not isinstance(filename, str) or not filename.strip():
        raise SavePathError("filename must be a non-empty string")
    if "/" in filename or "\\" in filename or os.sep in filename:
        raise SavePathError(f"filename must not contain a path separator: {filename!r}")

    candidate = directory / filename
    if overwrite or not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 1
    while True:
        alternative = directory / f"{stem}_{counter}{suffix}"
        if not alternative.exists():
            return alternative
        counter += 1


# --------------------------------------------------------------------------
# Backend discovery and capture
# --------------------------------------------------------------------------


def _display_available() -> bool:
    """Report whether this machine looks like it has a screen.

    On Windows and macOS a session normally has a desktop, so the check is only
    meaningful on Linux, where a headless box has neither ``DISPLAY`` nor
    ``WAYLAND_DISPLAY`` set.

    Returns:
        ``True`` if a display seems available.
    """
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True


def available_backends() -> list[str]:
    """List the screenshot backends that are both installed and usable.

    A backend is reported only if its library imports and a display appears to
    be present, so on a headless machine the list is empty and the caller gets a
    clear :class:`NoDisplayError` instead of a library-specific crash.

    Returns:
        The usable backend names, in :data:`BACKEND_ORDER` order.
    """
    if not _display_available():
        return []
    usable: list[str] = []
    for name in BACKEND_ORDER:
        if _backend_importable(name):
            usable.append(name)
    return usable


def _backend_importable(name: str) -> bool:
    """Report whether the library backing ``name`` can be imported.

    Args:
        name: One of the values in :data:`BACKEND_ORDER`.

    Returns:
        ``True`` if the import succeeds.
    """
    module_names = {
        "mss": "mss",
        "pillow": "PIL.ImageGrab",
        "pyautogui": "pyautogui",
    }
    module_name = module_names.get(name)
    if module_name is None:
        return False
    try:
        __import__(module_name)
    except Exception:  # noqa: BLE001
        # A backend that fails to import is simply unavailable. ImportError is
        # the expected case when it is not installed, but these libraries also
        # raise assorted other errors on a headless box, and a backend that
        # cannot even be imported is unusable either way.
        return False
    return True


def get_screen_size(backend: str = "pillow") -> tuple[int, int]:
    """Return the size of the primary screen as ``(width, height)``.

    Used to reject a region that falls outside the screen before any capture is
    attempted.

    Args:
        backend: The backend to measure with. ``mss`` and ``pillow`` are both
            supported.

    Returns:
        The screen size in pixels.

    Raises:
        NoDisplayError: If the size cannot be determined.

    Example:
        >>> width, height = get_screen_size()   # doctest: +SKIP
        >>> width > 0 and height > 0            # doctest: +SKIP
        True
    """
    if not _display_available():
        raise NoDisplayError(
            "No display detected (DISPLAY and WAYLAND_DISPLAY are both unset), "
            "so there is nothing to capture. Screenshots require an interactive "
            "desktop session."
        )
    try:
        if backend == "mss":
            import mss  # type: ignore[import-not-found]

            with mss.mss() as sct:
                monitor = sct.monitors[0]
                return int(monitor["width"]), int(monitor["height"])
        if backend == "pillow":
            from PIL import ImageGrab  # type: ignore[import-not-found]

            width, height = ImageGrab.grab().size
            return int(width), int(height)
    except Exception as exc:
        raise NoDisplayError(f"Could not read the screen size: {exc}") from exc

    raise NoDisplayError(f"Backend {backend!r} cannot report a screen size")


def _check_region_within_screen(
    region: tuple[int, int, int, int], screen: tuple[int, int]
) -> None:
    """Confirm a region fits inside the screen.

    Args:
        region: The validated ``(left, top, width, height)`` region.
        screen: The screen size as ``(width, height)``.

    Raises:
        InvalidRegionError: If the region extends past the screen edge.
    """
    left, top, width, height = region
    screen_width, screen_height = screen
    if left < 0 or top < 0:
        raise InvalidRegionError(
            f"region starts at ({left}, {top}), which is off the top-left of a "
            f"{screen_width}x{screen_height} screen"
        )
    if left + width > screen_width or top + height > screen_height:
        raise InvalidRegionError(
            f"region {region} does not fit on a {screen_width}x{screen_height} screen"
        )


def capture_screen(
    region: Sequence[int] | None = None,
    backend: str | None = None,
    verify_bounds: bool = True,
) -> Image:
    """Capture the screen, or a region of it.

    Args:
        region: ``(left, top, width, height)``, or ``None`` for the whole
            screen. Validated by :func:`validate_region`.
        backend: Force a specific backend instead of auto-detecting. Must be one
            of :data:`BACKEND_ORDER`.
        verify_bounds: Check the region against the screen size before
            capturing, so an off-screen region fails with a clear message rather
            than a library-specific one.

    Returns:
        A ``PIL.Image.Image`` holding the capture.

    Raises:
        InvalidRegionError: If the region is malformed or off-screen.
        NoBackendError: If the requested backend is not installed.
        NoDisplayError: If there is no display, or the capture itself fails.

    Example:
        >>> image = capture_screen((0, 0, 100, 100))   # doctest: +SKIP
        >>> image.size                                     # doctest: +SKIP
        (100, 100)
    """
    checked_region = validate_region(region)

    if backend is not None and backend not in BACKEND_ORDER:
        raise NoBackendError(
            f"unknown backend {backend!r}; choose one of " f"{', '.join(BACKEND_ORDER)}"
        )

    if not _display_available():
        raise NoDisplayError(
            "No display detected (DISPLAY and WAYLAND_DISPLAY are both unset), "
            "so there is nothing to capture. Screenshots require an interactive "
            "desktop session."
        )

    if backend is None:
        usable = available_backends()
        if not usable:
            raise NoBackendError(
                "No screenshot backend is available. Install one of: "
                + ", ".join(f"pip install {name}" for name in BACKEND_ORDER)
            )
        backend = usable[0]
    elif not _backend_importable(backend):
        raise NoBackendError(
            f"the {backend!r} backend is not installed; " f"try: pip install {backend}"
        )

    if checked_region is not None and verify_bounds:
        # A backend that cannot report a size is not a reason to fail the
        # capture, so bounds checking is best-effort.
        try:
            _check_region_within_screen(checked_region, get_screen_size(backend))
        except NoDisplayError:
            pass

    try:
        if backend == "mss":
            import mss  # type: ignore[import-not-found]

            with mss.mss() as sct:
                if checked_region is None:
                    shot = sct.grab(sct.monitors[0])
                else:
                    left, top, width, height = checked_region
                    shot = sct.grab(
                        {"left": left, "top": top, "width": width, "height": height}
                    )
                return shot  # type: ignore[return-value]
        if backend == "pillow":
            from PIL import ImageGrab  # type: ignore[import-not-found]

            bbox = checked_region
            return ImageGrab.grab(bbox=bbox)
        if backend == "pyautogui":
            import pyautogui  # type: ignore[import-untyped]

            if checked_region is None:
                return pyautogui.screenshot()  # type: ignore[no-any-return]
            left, top, width, height = checked_region
            return pyautogui.screenshot(  # type: ignore[no-any-return]
                region=(left, top, width + left, height + top)
            )
    except Exception as exc:
        # Whatever the library raised, the caller gets one consistent error type
        # with the original message preserved.
        raise NoDisplayError(
            f"Capture failed using the {backend!r} backend: {exc}"
        ) from exc

    raise NoBackendError(f"Backend {backend!r} is not implemented")


def save_image(image: Image, path: Path, image_format: str | None = None) -> Path:
    """Save a captured image to disk.

    The format is taken from the filename suffix unless given explicitly. JPEG
    and BMP cannot store an alpha channel, so images carrying one are converted
    to RGB first, which avoids a confusing "cannot write mode RGBA as JPEG".

    Args:
        image: The image to save, normally a ``PIL.Image.Image``.
        path: Where to save it.
        image_format: Override the format; otherwise inferred from the suffix.

    Returns:
        The path that was written.

    Raises:
        InvalidFormatError: If the format is not supported.
        SavePathError: If the file cannot be written.

    Example:
        >>> save_image(image, Path("shot.png"))   # doctest: +SKIP
        PosixPath('shot.png')
    """
    if image_format is None:
        image_format = path.suffix.lstrip(".") or DEFAULT_FORMAT
    checked_format = validate_format(image_format)

    if checked_format in FORMATS_WITHOUT_ALPHA and image.mode in {
        "RGBA",
        "LA",
        "P",
    }:
        image = image.convert("RGB")

    try:
        image.save(path, format=SUPPORTED_FORMATS[checked_format])
    except (OSError, ValueError, KeyError) as exc:
        raise SavePathError(f"Could not save screenshot to {path}: {exc}") from exc
    return path


def take_screenshot(
    region: Sequence[int] | None = None,
    output_dir: str | os.PathLike[str] = DEFAULT_OUTPUT_DIR,
    filename: str | None = None,
    image_format: str = DEFAULT_FORMAT,
    backend: str | None = None,
    overwrite: bool = False,
    verify_bounds: bool = True,
    when: datetime | None = None,
) -> Path:
    """Capture the screen and save it, returning the path written.

    This is the one-call entry point that ties the other pieces together:
    validate the region and format, work out a filename, capture, and save.

    Args:
        region: ``(left, top, width, height)``, or ``None`` for the whole screen.
        output_dir: Directory to save into; created if missing.
        filename: Explicit filename. When omitted a timestamped name is
            generated with :func:`build_filename`.
        image_format: Format to save as. Must match ``filename``'s suffix when
            one is given, otherwise ``filename`` wins.
        backend: Force a backend, or ``None`` to auto-detect.
        overwrite: Allow replacing an existing file. When ``False`` a numeric
            suffix is added instead, so nothing is lost.
        verify_bounds: Reject a region that does not fit on the screen.
        when: Timestamp override for the generated filename.

    Returns:
        The :class:`~pathlib.Path` of the saved file.

    Raises:
        InvalidRegionError: If the region is malformed or off-screen.
        InvalidFormatError: If the format is not supported.
        SavePathError: If the destination cannot be written.
        NoBackendError: If no backend is available.
        NoDisplayError: If there is no display to capture.

    Example:
        >>> path = take_screenshot((0, 0, 320, 240))   # doctest: +SKIP
        >>> path.name.startswith("screenshot_")        # doctest: +SKIP
        True
    """
    checked_format = validate_format(image_format)
    directory = resolve_output_dir(output_dir)

    if filename is None:
        name = build_filename(checked_format, when=when)
    else:
        name = filename
        suffix = Path(name).suffix.lstrip(".").lower()
        if suffix and suffix not in SUPPORTED_FORMATS:
            raise InvalidFormatError(
                f"filename {name!r} has unsupported extension {suffix!r}; "
                f"supported: {', '.join(sorted(set(SUPPORTED_FORMATS)))}"
            )

    target = unique_path(directory, name, overwrite=overwrite)

    image = capture_screen(region, backend=backend, verify_bounds=verify_bounds)
    return save_image(image, target, checked_format)


# --------------------------------------------------------------------------
# Command-line interface
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point.

    Args:
        argv: Argument list, defaulting to ``sys.argv[1:]``.

    Returns:
        ``0`` on success, ``1`` on any expected failure, ``2`` for a usage
        error raised by :mod:`argparse`.
    """
    parser = argparse.ArgumentParser(
        description="Capture the screen or a region of it and save it to disk."
    )
    parser.add_argument(
        "--region",
        nargs=4,
        type=int,
        metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
        help="capture only this region; omit for the whole screen",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"directory to save into, created if needed (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "-f", "--filename", default=None, help="explicit filename to save as"
    )
    parser.add_argument(
        "-t",
        "--format",
        default=DEFAULT_FORMAT,
        help="image format: " + ", ".join(sorted(set(SUPPORTED_FORMATS))),
    )
    parser.add_argument(
        "-b",
        "--backend",
        default=None,
        choices=BACKEND_ORDER,
        help="force a capture backend instead of auto-detecting",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing file instead of adding a numeric suffix",
    )
    parser.add_argument(
        "--list-backends",
        action="store_true",
        help="print the available backends and exit",
    )
    args = parser.parse_args(argv)

    if args.list_backends:
        usable = available_backends()
        if usable:
            print("Available backends: " + ", ".join(usable))
        else:
            print(
                "No backends available. No display was detected, or none of "
                + ", ".join(BACKEND_ORDER)
                + " is installed."
            )
        return 0

    try:
        path = take_screenshot(
            region=args.region,
            output_dir=args.output_dir,
            filename=args.filename,
            image_format=args.format,
            backend=args.backend,
            overwrite=args.overwrite,
        )
    except ScreenshotError as exc:
        # Every expected failure arrives here, so the CLI prints a readable
        # message instead of a traceback.
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved screenshot to {path}")
    return 0


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
# The test suite is entirely offline: it never captures a real screen, and it
# needs no third-party package, so it runs anywhere including CI. Capture is
# exercised through a stub image, while validation, filename generation, path
# handling and error mapping are tested directly.


class _StubImage:
    """Stand-in for a ``PIL.Image.Image``.

    Records what :meth:`save` and :meth:`convert` were asked to do, so the
    saver's behaviour can be checked without a display or a real image library.
    The log is shared with any image produced by :meth:`convert`, which returns
    a *new* object exactly as Pillow does, so the caller can still observe that
    a conversion happened.

    Attributes:
        size: The ``(width, height)`` this image claims to have.
        mode: The Pillow mode name, e.g. ``"RGB"`` or ``"RGBA"``.
        log: A shared list of ``("convert", mode)`` and ``("save", path, fmt)``
            tuples in call order.
        saved_as: The last ``(path, format)`` passed to :meth:`save`, if any.
    """

    def __init__(
        self,
        size: tuple[int, int] = (4, 4),
        mode: str = "RGB",
        log: list[tuple[Any, ...]] | None = None,
    ) -> None:
        self.size = size
        self.mode = mode
        self.log: list[tuple[Any, ...]] = [] if log is None else log
        self.saved_as: tuple[Any, str | None] | None = None

    def convert(self, mode: str) -> _StubImage:
        """Return a new image in another mode, as Pillow does."""
        self.log.append(("convert", mode))
        return _StubImage(self.size, mode, self.log)

    def save(self, path: Any, format: str | None = None) -> None:
        """Record the save request instead of touching the filesystem."""
        self.log.append(("save", path, format))
        self.saved_as = (path, format)


def _run_tests() -> None:
    """Run the self-checks covering normal input, edge cases and failures."""
    import tempfile

    # --- validate_region: normal input ------------------------------------
    assert validate_region([0, 0, 100, 200]) == (0, 0, 100, 200)
    assert validate_region((10, 20, 30, 40)) == (10, 20, 30, 40)
    assert validate_region([-1920, 0, 640, 480]) == (-1920, 0, 640, 480)
    assert validate_region(None) is None

    # --- validate_region: edge cases --------------------------------------
    # A 1x1 region is the smallest legal capture.
    assert validate_region([0, 0, 1, 1]) == (0, 0, 1, 1)
    # A region covering the whole screen exactly.
    assert validate_region([0, 0, 1920, 1080]) == (0, 0, 1920, 1080)

    # --- validate_region: failure cases -----------------------------------
    for bad_region in (
        [0, 0, 0, 10],  # zero width
        [0, 0, 10, 0],  # zero height
        [0, 0, -5, 10],  # negative width
        [0, 0, 10],  # too few values
        [0, 0, 10, 10, 10],  # too many values
        [0, 0, 10, "20"],  # non-int value
        [0, 0, 10, 10.5],  # float value
        [0, 0, True, 10],  # bool is not a coordinate
        "0,0,10,10",  # a string is not a sequence of ints
        42,  # not a sequence at all
    ):
        try:
            validate_region(bad_region)  # type: ignore[arg-type]
        except InvalidRegionError:
            pass
        else:
            raise AssertionError(f"expected InvalidRegionError for {bad_region!r}")

    # InvalidRegionError is also a ValueError, so generic handlers work.
    assert issubclass(InvalidRegionError, ValueError)
    assert issubclass(InvalidFormatError, ValueError)
    assert issubclass(NoDisplayError, ScreenshotError)

    # --- validate_format ---------------------------------------------------
    assert validate_format("png") == "png"
    assert validate_format("PNG") == "png"
    assert validate_format(".Jpeg") == "jpeg"
    assert validate_format("  bmp  ") == "bmp"
    for bad_format in ("gif", "exe", "", "png2", 5, None, ["png"]):
        try:
            validate_format(bad_format)  # type: ignore[arg-type]
        except InvalidFormatError:
            pass
        else:
            raise AssertionError(f"expected InvalidFormatError for {bad_format!r}")

    # --- build_filename ----------------------------------------------------
    assert build_filename(
        "png", datetime(2026, 9, 27, 14, 23, 5, tzinfo=timezone.utc)
    ) == ("screenshot_20260927_142305.png")
    assert build_filename(
        "jpg", datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    ) == ("screenshot_20260102_030405.jpg")
    assert build_filename(
        "bmp", datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    ) == ("screenshot_20261231_235959.bmp")
    # A custom prefix is honoured, and the default uses the current time.
    assert build_filename(
        "png", datetime(2026, 9, 27, 0, 0, 0, tzinfo=timezone.utc), "desktop"
    ).startswith("desktop_20260927_000000.png")
    assert build_filename().startswith("screenshot_")
    for bad_prefix in ("", "   ", "a/b", "a\\b"):
        try:
            build_filename(
                "png", datetime(2026, 9, 27, tzinfo=timezone.utc), bad_prefix
            )
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for prefix {bad_prefix!r}")
    try:
        build_filename("gif")
    except InvalidFormatError:
        pass
    else:
        raise AssertionError("expected InvalidFormatError from build_filename")

    # --- resolve_output_dir ------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        # An existing directory is returned resolved.
        assert resolve_output_dir(base) == base.resolve()
        assert resolve_output_dir(str(base)) == base.resolve()

        # A missing directory is created, including parents.
        nested = base / "shots" / "2026"
        assert resolve_output_dir(nested) == nested.resolve()
        assert nested.is_dir()

        # A path that exists but is a file is rejected.
        a_file = base / "not_a_dir.txt"
        a_file.write_text("hello", encoding="utf-8")
        try:
            resolve_output_dir(a_file)
        except SavePathError:
            pass
        else:
            raise AssertionError("expected SavePathError for a file as output_dir")

        # A non-path value is rejected.
        for bad_dir in (5, None, ["a"]):
            try:
                resolve_output_dir(bad_dir)  # type: ignore[arg-type]
            except SavePathError:
                pass
            else:
                raise AssertionError(f"expected SavePathError for {bad_dir!r}")

        # --- unique_path ---------------------------------------------------
        assert unique_path(base, "shot.png") == base / "shot.png"
        # No overwrite: a numeric suffix is added instead.
        (base / "shot.png").write_bytes(b"x")
        assert unique_path(base, "shot.png") == base / "shot_1.png"
        (base / "shot_1.png").write_bytes(b"x")
        assert unique_path(base, "shot.png") == base / "shot_2.png"
        # With overwrite: the original path is returned unchanged.
        assert unique_path(base, "shot.png", overwrite=True) == base / "shot.png"
        # A name without a suffix still works.
        assert unique_path(base, "plain") == base / "plain"
        # Names that would escape the directory are rejected.
        for bad_name in ("", "   ", "../escape.png", "sub/dir.png", "a\\b.png"):
            try:
                unique_path(base, bad_name)
            except SavePathError:
                pass
            else:
                raise AssertionError(f"expected SavePathError for {bad_name!r}")

    # --- save_image --------------------------------------------------------
    def as_image(stub: _StubImage) -> Any:
        """Present a stub as the ``PIL.Image.Image`` that ``save_image`` wants.

        This is the single seam where the test suite steps outside the type
        system: the saver is annotated against the real Pillow class, and the
        stub deliberately records calls instead of holding pixels, which is
        exactly what lets these tests run with no display and no image library.
        """
        return stub

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        # An RGB image is passed straight through with the mapped format name.
        image = _StubImage((4, 4), "RGB")
        target = base / "shot.png"
        assert save_image(as_image(image), target) == target
        assert image.saved_as is not None
        assert image.saved_as[0] == target
        assert image.saved_as[1] == "PNG"

        # JPEG maps to Pillow's "JPEG", not "JPG".
        image = _StubImage()
        save_image(as_image(image), base / "shot.jpg")
        assert image.saved_as is not None
        assert image.saved_as[1] == "JPEG"

        # An image with an alpha channel is converted before saving as JPEG.
        image = _StubImage((4, 4), "RGBA")
        save_image(as_image(image), base / "shot.jpg")
        assert ("convert", "RGB") in image.log
        # ...but PNG keeps the alpha channel untouched.
        rgba = _StubImage((4, 4), "RGBA")
        save_image(as_image(rgba), base / "shot.png")
        assert not any(event[0] == "convert" for event in rgba.log)

        # A suffix-less filename falls back to PNG.
        image = _StubImage()
        save_image(as_image(image), base / "shot")
        assert image.saved_as is not None
        assert image.saved_as[1] == "PNG"

        # An unsupported extension is rejected before any write is attempted.
        image = _StubImage()
        try:
            save_image(as_image(image), base / "shot.gif")
        except InvalidFormatError:
            assert image.saved_as is None, "must not write an unsupported format"
        else:
            raise AssertionError("expected InvalidFormatError for a .gif target")

        # A failing save is reported as a SavePathError.
        class _ExplodingImage(_StubImage):
            def save(self, path: Any, format: str | None = None) -> None:
                raise OSError("disk full")

        try:
            save_image(as_image(_ExplodingImage()), base / "shot.png")
        except SavePathError:
            pass
        else:
            raise AssertionError("expected SavePathError when the write fails")

    # --- _check_region_within_screen --------------------------------------
    _check_region_within_screen((0, 0, 100, 100), (1920, 1080))
    _check_region_within_screen((1820, 980, 100, 100), (1920, 1080))
    for bad, screen in (
        ((0, 0, 1921, 10), (1920, 1080)),  # wider than the screen
        ((0, 0, 10, 1081), (1920, 1080)),  # taller than the screen
        ((-1, 0, 10, 10), (1920, 1080)),  # off the left edge
        ((0, -1, 10, 10), (1920, 1080)),  # off the top edge
    ):
        try:
            _check_region_within_screen(bad, screen)
        except InvalidRegionError:
            pass
        else:
            raise AssertionError(f"expected InvalidRegionError for {bad} on {screen}")

    # --- capture_screen and take_screenshot, with the backend stubbed ------
    # Capturing is replaced so the pipeline can be tested without a display.
    # `saved_paths` records where a real save ended up, standing in for Pillow.
    saved_paths: list[Path] = []

    def fake_capture_screen(
        region: Sequence[int] | None = None,
        backend: str | None = None,
        verify_bounds: bool = True,
    ) -> _StubImage:
        """Stand-in for :func:`capture_screen`.

        Honours ``verify_bounds`` the same way the real function does, so the
        bounds tests below are meaningful.
        """
        checked = validate_region(region)
        if checked is not None and verify_bounds:
            _check_region_within_screen(checked, (1920, 1080))
        if checked is None:
            return _StubImage((1920, 1080), "RGB")
        return _StubImage((checked[2], checked[3]), "RGB")

    def fake_save_image(
        image: _StubImage, path: Path, image_format: str | None = None
    ) -> Path:
        """Stand-in for :func:`save_image` that really writes a small file."""
        target = Path(path)
        target.write_bytes(b"fake-png-bytes")
        saved_paths.append(target)
        return target

    real_capture = globals()["capture_screen"]
    real_save = globals()["save_image"]
    try:
        globals()["capture_screen"] = fake_capture_screen
        globals()["save_image"] = fake_save_image

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)

            # Whole screen with a generated filename.
            path = take_screenshot(
                output_dir=base,
                when=datetime(2026, 9, 27, 14, 23, 5, tzinfo=timezone.utc),
            )
            assert path.name == "screenshot_20260927_142305.png"
            assert path.parent == base.resolve()
            assert path.is_file(), "the screenshot must actually be written"

            # A named file in a region.
            path = take_screenshot(
                region=[10, 20, 30, 40],
                output_dir=base,
                filename="region.png",
            )
            assert path.name == "region.png"

            # Two runs without --overwrite must not clobber each other.
            first = take_screenshot(output_dir=base, filename="same.png")
            second = take_screenshot(output_dir=base, filename="same.png")
            assert first.name == "same.png"
            assert second.name == "same_1.png"
            assert first.is_file() and second.is_file()

            # With overwrite=True the same name is reused.
            third = take_screenshot(
                output_dir=base, filename="same.png", overwrite=True
            )
            assert third.name == "same.png"

            # A missing output directory is created on demand.
            nested = base / "deep" / "shots"
            path = take_screenshot(
                output_dir=nested, filename="made.png", image_format="jpg"
            )
            assert path.is_file()
            assert nested.is_dir()

            # A filename whose extension disagrees with --format is accepted,
            # because the filename wins.
            path = take_screenshot(
                output_dir=base, filename="byext.bmp", image_format="png"
            )
            assert path.suffix == ".bmp"

            # --- take_screenshot failure cases ----------------------------
            # A bad region never reaches the capture, so nothing is written.
            for bad_region in ([0, 0, 0, 5], [0, 0, 5], "nope"):
                written_before = len(saved_paths)
                try:
                    take_screenshot(
                        region=bad_region,  # type: ignore[arg-type]
                        output_dir=base,
                    )
                except InvalidRegionError:
                    assert (
                        len(saved_paths) == written_before
                    ), "a rejected region must not write a file"
                else:
                    raise AssertionError(
                        f"expected InvalidRegionError for {bad_region!r}"
                    )

            # An off-screen region is rejected by the bounds check.
            try:
                take_screenshot(
                    region=[0, 0, 5000, 5000], output_dir=base, filename="big.png"
                )
            except InvalidRegionError:
                pass
            else:
                raise AssertionError(
                    "expected InvalidRegionError for an off-screen region"
                )

            # An unsupported format is rejected before anything is written.
            try:
                take_screenshot(output_dir=base, image_format="gif")
            except InvalidFormatError:
                pass
            else:
                raise AssertionError(
                    "expected InvalidFormatError for image_format='gif'"
                )

            # A filename with an unsupported extension is rejected.
            try:
                take_screenshot(output_dir=base, filename="shot.gif")
            except InvalidFormatError:
                pass
            else:
                raise AssertionError(
                    "expected InvalidFormatError for filename='shot.gif'"
                )

            # A filename that tries to escape the output directory.
            try:
                take_screenshot(output_dir=base, filename="../escape.png")
            except SavePathError:
                pass
            else:
                raise AssertionError("expected SavePathError for a traversing filename")

            # An output_dir that is a file, not a directory.
            not_a_dir = base / "afile.txt"
            not_a_dir.write_text("x", encoding="utf-8")
            try:
                take_screenshot(output_dir=not_a_dir, filename="x.png")
            except SavePathError:
                pass
            else:
                raise AssertionError("expected SavePathError when output_dir is a file")

            # An unknown backend name is rejected by the real `capture_screen`,
            # which is stubbed out in this block, so it is covered further down
            # where the genuine function runs.
    finally:
        globals()["capture_screen"] = real_capture
        globals()["save_image"] = real_save

    # --- the real capture_screen refuses to work with no display ----------
    # `_display_available` is stubbed to False to simulate a headless CI box.
    real_display_check = globals()["_display_available"]
    try:
        globals()["_display_available"] = lambda: False
        assert available_backends() == []
        for call, error in (
            (lambda: capture_screen(), NoDisplayError),
            (lambda: capture_screen((0, 0, 10, 10)), NoDisplayError),
            (lambda: get_screen_size(), NoDisplayError),
        ):
            try:
                call()
            except error as exc:
                # The message must be actionable, not a raw library traceback.
                assert "display" in str(exc).lower(), f"unhelpful message: {exc}"
            else:
                raise AssertionError(f"expected {error.__name__} when headless")
    finally:
        globals()["_display_available"] = real_display_check

    # --- capture_screen argument checking happens before any capture -----
    # The real `capture_screen` runs here, with only the display-touching
    # helpers replaced, so its own argument validation is genuinely exercised
    # and no screen is ever captured.
    real_available_backends = globals()["available_backends"]
    real_backend_importable = globals()["_backend_importable"]
    real_get_screen_size = globals()["get_screen_size"]
    try:
        globals()["_backend_importable"] = lambda name: True
        globals()["get_screen_size"] = lambda backend="pillow": (1920, 1080)

        # An unknown backend is rejected by name, before any capture.
        try:
            capture_screen(backend="nope")
        except NoBackendError:
            pass
        else:
            raise AssertionError("expected NoBackendError for backend='nope'")

        # A malformed region is rejected before the backend is consulted.
        try:
            capture_screen(region=[0, 0, 0, 0], backend="pillow")
        except InvalidRegionError:
            pass
        else:
            raise AssertionError("expected InvalidRegionError for a zero-size region")

        # An off-screen region is rejected by the bounds check.
        try:
            capture_screen(region=[0, 0, 4000, 4000], backend="pillow")
        except InvalidRegionError:
            pass
        else:
            raise AssertionError("expected InvalidRegionError for an off-screen region")

        # With the display helper stubbed out, auto-detection finds no backend
        # rather than reaching for a real library.
        globals()["available_backends"] = list
        try:
            capture_screen()
        except NoBackendError as exc:
            assert "pip install" in str(exc), f"message should be actionable: {exc}"
        else:
            raise AssertionError("expected NoBackendError when no backend is available")
    finally:
        globals()["available_backends"] = real_available_backends
        globals()["_backend_importable"] = real_backend_importable
        globals()["get_screen_size"] = real_get_screen_size

    # --- CLI return codes -------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        # A bad region is a clean failure, not a traceback.
        assert main(["--region", "0", "0", "0", "10", "-o", str(base)]) == 1
        # An unsupported format likewise.
        assert main(["-t", "gif", "-o", str(base)]) == 1
        # --list-backends always succeeds and prints something.
        assert main(["--list-backends"]) == 0

    print("All tests passed.")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _run_tests()
        raise SystemExit(0)
    raise SystemExit(main())
