from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class DigitalContent(models.Model):
    name = models.CharField(max_length=100)
    access_by = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Registered Resources Table
class RegisteredResource(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(DigitalContent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username.username} - {self.content.name}"