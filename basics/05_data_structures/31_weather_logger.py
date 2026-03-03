import python_weather  # Library to fetch weather data in Python
import asyncio
from datetime import datetime


async def main() -> None:
    """
    Main function to:
    - fetch today's weather for a city
    - store it in a nested dictionary (date -> {temp, condition, humidity})
    - find the hottest day
    - calculate the average temperature
    - display the full weather log
    """

    # Create a weather client. unit=IMPERIAL uses Fahrenheit and mph
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        
        # Fetch the weather forecast for Rome
        cityForecast = await client.get('Rome')
        
        # Main dictionary to store daily weather logs
        weather_log = {}

        # Get today's date in YYYY-MM-DD format
        date = datetime.today().strftime('%Y-%m-%d')

        # Add a new entry for today
        # Key = date, Value = dictionary with temperature, condition, and humidity
        weather_log[date] = {
            "temp": cityForecast.temperature,
            "condition": cityForecast.description,
            "humidity": cityForecast.humidity
        }

        # Print the raw dictionary for debugging/verification
        print("Weather log:", weather_log, "\n")

        # Find the hottest day
        # The lambda tells Python to compare the 'temp' values of each date
        hottest_day = max(weather_log, key=lambda d: weather_log[d]["temp"])

        # Calculate the average temperature
        # Sum all temperatures and divide by the number of entries
        avg_temp = sum(day["temp"] for day in weather_log.values()) / len(weather_log)

        # Print the hottest day and the average temperature
        print(f"The hottest day was {hottest_day}")
        print(f"The average temperature is {avg_temp:.2f}°F")  # formatted to 2 decimals


if __name__ == '__main__':
    asyncio.run(main())
