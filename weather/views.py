import datetime
import re

from django.core.cache import cache
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.models import PincodeLocation, WeatherDetails
from weather.services import (
    convert_date_to_unix,
    get_lat_long_from_pincode,
    get_weather_details,
)
from weather.tasks import store_pincode_location, store_weather_data

# Create your views here.


class GetWeatherViaPincode(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "pincode",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The pincode for which to get the weather. Must be a valid Indian pincode.",
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The date for which to get the weather. Must be in YYYY-MM-DD format.",
            ),
        ],
        operation_summary="Get weather details based on pincode and date",
        operation_description="This endpoint returns the weather details for a given pincode and date. The date must be in the past.",
        responses={
            200: openapi.Response(
                "Weather details",
                schema=openapi.Schema(type=openapi.TYPE_OBJECT),
            )
        },
    )
    def get(self, request):
        pincode = request.query_params.get("pincode")
        date = request.query_params.get("date")
        if date:
            # validates date, converts it into ist and then converts it into unix time
            unix_date = convert_date_to_unix(date)
        else:
            return Response(
                {"error": "Please provide a valid date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pincode_validation_regex = "^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$"

        if not pincode or not re.match(pincode_validation_regex, pincode):
            return Response(
                {"error": "Please provide a valid pincode"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if weather data is in cache
        weather_data = cache.get(f"weather_data_{pincode}_{unix_date}")

        # check if weather data is in db
        weather_data = WeatherDetails.objects.filter(
            pincode=pincode, date=datetime.datetime.fromtimestamp(unix_date)
        ).first()

        if weather_data:
            return Response(weather_data, status=status.HTTP_200_OK)

        # Check if location data is in cache
        location_data = cache.get(f"location_data_{pincode}")
        if not location_data:
            # Check if pincode in our db
            pincode_location = PincodeLocation.objects.filter(
                pincode=pincode
            ).first()
            if pincode_location:
                location_data = {
                    "latitude": pincode_location.latitude,
                    "longitude": pincode_location.longitude,
                }
            else:
                # Calling service to fetch latitude and longitude based on pincode
                latitude, longitude = get_lat_long_from_pincode(pincode)
                if not latitude or not longitude:
                    return Response(
                        {"error": "Error fetching latitude and longitude"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                # Save pincode location in db asynchronously
                store_pincode_location.delay(pincode, latitude, longitude)

                location_data = {"latitude": latitude, "longitude": longitude}

            # Save location data in cache
            cache.set(f"location_data_{pincode}", location_data)

        # Fetch weather data, save it in cache and return it
        weather_data = get_weather_details(
            location_data["latitude"], location_data["longitude"], unix_date
        )
        # Save weather data in cache
        cache.set(f"weather_data_{pincode}_{unix_date}", weather_data)

        # Save weather data in db asynchronously
        store_weather_data.delay(pincode, unix_date, weather_data)

        return Response(weather_data, status=status.HTTP_200_OK)
