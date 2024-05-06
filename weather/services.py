import datetime

import pytz
import requests
from django.conf import settings

api_key = settings.OPEN_WEATHER_API_KEY


# Function to get latitude and longitude from pincode
def get_lat_long_from_pincode(pincode):
    try:
        get_lat_long_api = f"http://api.openweathermap.org/geo/1.0/zip?zip={pincode},IN&appid={api_key}"
        location = requests.get(get_lat_long_api)
        if location.status_code == 200:
            location = location.json()
        else:
            raise ValueError(
                "Error getting latitude and longitude from pincode: %s"
            )

        if location:
            return (location["lat"], location["lon"])
        else:
            return (None, None)
    except Exception as e:
        raise ValueError(
            "Error getting latitude and longitude from pincode: %s" % e
        )


def get_weather_details(lat, lon, unix_date):
    try:
        get_weather_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt=1714521600&appid=8a8807cab300236f46d31c42e95b2181"
        response = requests.get(get_weather_url)
        print(response.status_code)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        raise ValueError("Error getting weather details: %s" % e)


def convert_date_to_unix(date_string):
    try:
        dt = datetime.datetime.strptime(date_string, "%Y-%m-%d")

        # convert to IST
        ist = pytz.timezone("Asia/Kolkata")
        dt = ist.localize(dt)

        # convert to UTC
        dt = dt.astimezone(pytz.UTC)

        unix_time = dt.timestamp()
        return int(unix_time)
    except ValueError:
        raise ValueError(
            "Invalid date format. Please provide date in YYYY-MM-DD format"
        )
    except Exception as e:
        raise ValueError("Error converting date to unix time: %s" % e)
