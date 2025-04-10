from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Event(models.Model):
    ACCESS_CHOICES = [
        ('community holder', 'Community Holder'),
        ('create workspace holder', 'Create Workspace Holder'),
        ('key access holder', 'Key Access Holder'),
        ('guest', 'Guest'),
    ]

    eventname = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    access_by = models.CharField(
        max_length=50,
        choices=ACCESS_CHOICES,
        default='guest'
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # Optional field
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.eventname

class RegisteredEvent(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username.username} - {self.event.eventname}"