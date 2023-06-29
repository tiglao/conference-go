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


#function 2:
#request to use Open Weather API
def get_weather_data(city, state):
    pass
