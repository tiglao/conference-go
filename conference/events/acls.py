import json
import requests

from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def grab_image(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": f"{city} {state}",
        "per_page": 1,
    }
    url = "https://api.pexels.com/v1/search"
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    try:
        return {"image_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"image_url":  None}


def grab_coordinates(city, state):
    params = {
        "q": f"{city}, {state}, US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = "http://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    try:
        return {
            "lat": content[0]["lat"],
            "lon": content[0]["lon"],
        }
    except (KeyError, IndexError):
        return {
            "lat": None,
            "lon": None,
        }


def grab_weather(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    print("THE GRAB_WEATHER app is working", content)
    # try:
    #     return {"weather": content["weather"][0]["description"]}
    # except (KeyError, IndexError):
    #     return {"weather": None}
