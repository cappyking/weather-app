from django.urls import path
from weather.views import GetWeatherViaPincode
urlpatterns = [
    path("get-weather-via-pincode/", GetWeatherViaPincode.as_view(), name="get-weather-via-pincode"),
]
