from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Event(models.Model):
    eventname = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    access_by = models.CharField(max_length=100)

    def __str__(self):
        return self.eventname

# Registered Events Table
class RegisteredEvent(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username.username} - {self.event.eventname}"