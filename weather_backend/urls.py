"""
URL configuration for FFWeather project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/weather/", include("weather.urls")),
]

schema_view=get_schema_view(
    openapi.Info(
        title="FFWeather API",
        default_version="v1",
        description="FFWeather API to get weather via pincode",
    ),
    public=True,
    patterns=urlpatterns,
)
urlpatterns += [
  path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),]