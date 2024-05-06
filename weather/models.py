from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PincodeLocation(BaseModel):
    pincode = models.CharField(max_length=6, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.pincode} - {self.latitude},{self.longitude}"


class WeatherDetails(BaseModel):
    pincode = models.ForeignKey(PincodeLocation, on_delete=models.CASCADE)
    date = models.DateField()
    weather = models.JSONField()

    def __str__(self):
        return f"{self.pincode} - {self.date} - {self.weather}"