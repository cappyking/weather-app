from django.contrib import admin
from .models import PincodeLocation, WeatherDetails

class PincodeLocationAdmin(admin.ModelAdmin):
    list_display = ['pincode', 'latitude', 'longitude', 'created_at', 'updated_at']
    search_fields = ['pincode']

admin.site.register(PincodeLocation, PincodeLocationAdmin)

class WeatherDetailsAdmin(admin.ModelAdmin):
    list_display = ['pincode', 'date', 'weather', 'created_at', 'updated_at']
    search_fields = ['pincode__pincode', 'date']
    list_filter = ['date']

admin.site.register(WeatherDetails, WeatherDetailsAdmin)