from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    primary_number = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Appointment Model
class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    appointment_datetime = models.DateTimeField()
    account_holder_id = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('Confirmed', 'Confirmed'), ('Canceled', 'Canceled')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.appointment_datetime}"
