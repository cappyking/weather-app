import datetime

from celery import shared_task

from weather.models import PincodeLocation, WeatherDetails


@shared_task
def store_pincode_location(pincode, latitude, longitude):
    pincode_location = PincodeLocation(
        pincode=pincode, latitude=latitude, longitude=longitude
    )
    pincode_location.save()
    return True


@shared_task
def store_weather_data(pincode, unix_date, weather_data):
    date = datetime.datetime.fromtimestamp(unix_date)
    weather_data = WeatherDetails(
        pincode=pincode, date=date, weather_data=weather_data
    )
    weather_data.save()
    return True
