import requests
import sys
from requests.exceptions import HTTPError, ConnectionError, Timeout, TooManyRedirects, RequestException

"""Using Open-Meteo API, this Python app prompts the user for a city and state, then prints 
the next ten days of forecast showing the minimum and maximum temperature in Fahrenheit and 
the daily rainfall in inches."""

def get_coordinates(city, state):
    """Using Open-Meteo Geocoding API, converts City and State to Latitude/Longitude."""

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&admin1={state}&count=10&language=en&format=json"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data:
        print(f"Error: No results returned for '{city}, {state}'")
        sys.exit()

    result = None
    for loc in geo_data["results"]:
        # Check if state name or abbreviation matches (e.g., "Tennessee" or "TN")
        # .get('admin1', '') safely gets the state name
        if state.lower() in loc.get('admin1', '').lower() and city.lower() in loc.get('name', '').lower():
            result = loc
            break

    # Extract coordinates and location details
    if not result:
        print(f"Error: Could not find location '{city}, {state}'")
        sys.exit()

    lat = result["latitude"]
    lon = result["longitude"]
    return lat, lon

def get_weather(lat, lon, city, state):
    """Fetches 10-day forecast in Fahrenheit and inches using Open-Meteo Forecast API.
    """
    print("--- 10-Day Weather Forecast ---")
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": 10
    }

    try:
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred for {weather_url}: {http_err}") # e.g., 404 Not Found
    except ConnectionError as conn_err:
        print(f"Connection error occurred for {weather_url}: {conn_err}") # e.g., DNS failure, no internet
    except Timeout as timeout_err:
        print(f"Timeout error occurred for {weather_url}: {timeout_err}") # Server took too long to respond
    except TooManyRedirects as redirects_err:
        print(f"Too many redirects for {weather_url}: {redirects_err}")
    except RequestException as e:
        print(f"An general error occurred for {weather_url}: {e}") # Catches all other requests exceptions

    weather = response.json() # Get the JSON response from the API
    daily = weather['daily']

    print(f"\n10-Day Forecast for {city.title()}, {state.title()}:")
    print(f"{'Date':<12} | {'Max Temp':<10} | {'Min Temp':<10} | {'Rain (in)'}")
    print("-" * 55)

    for i in range(len(daily['time'])): # iterate through each day in the forecast
        date = daily['time'][i]
        t_max = daily['temperature_2m_max'][i]
        t_min = daily['temperature_2m_min'][i]
        rain = daily['precipitation_sum'][i]
        print(f"{date:<12} | {t_max:>5}°F    | {t_min:>5}°F    | {rain:.2f} in")

if __name__ == "__main__":
    try:
        city_name = input("Enter city name: ").strip()
        state_name = input("Enter state name: ").strip()
        lat, lon = get_coordinates(city_name, state_name)
        get_weather(lat, lon, city_name, state_name)
    except Exception as e:
        print(e)
