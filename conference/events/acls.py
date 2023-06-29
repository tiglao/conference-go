import json
import requests

from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def get_photo(city, state):
    headers = {
        "Authorization": PEXELS_API_KEY,
    }
    params = {
        "query": f"{city}, {state}",
        "per_page": 1,
    }
    url = "https://api.pexels.com/v1/search"
    response = requests.get(url, headers=headers, params=params)
    content = json.loads(response.content)
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    geocache_params = {
        "q": f"{city},{state},US",
        "appid": OPEN_WEATHER_API_KEY,
        "limit": 1,
    }
    geocache_api_url = "http://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(geocache_api_url, params=geocache_params)
    geocache_content = json.loads(response.content)
    lat = geocache_content[0]["lat"]
    lon = geocache_content[0]["lon"]
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY
    }
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    temp = content["main"]["temp"]
    description = content["weather"][0]["description"]
    try:
        return {
            "temp": temp,
            "description": description,
        }
    except (KeyError, ValueError):
        return {"weather": None}
