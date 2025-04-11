from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image  # Import Pillow for image handling
User = get_user_model()


# Create your models here.
class DigitalContent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    access_by = models.CharField(max_length=100)
    image = models.ImageField(upload_to='digitalcontent/images/', default='profile_images/membership_sample_page.jpg')  # Updated default to use the sample image
    created_by = models.CharField(max_length=100, default="admin")  # New column added

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img = img.resize((300, 300))  # Resize the image to 300x300
            img.save(self.image.path)

    def __str__(self):
        return self.name

# Registered Resources Table
class RegisteredContent(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(DigitalContent, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username.username} - {self.content.name}"