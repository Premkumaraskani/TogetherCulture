from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")
    interests = models.JSONField()

# class admin(models.Model):
#     id = models.AutoField(primary_key=True) 
#     name=models.CharField(max_length=50)    
#     password=models.CharField(max_length=50)    


    class Meta:
        db_table = "users"
        # db_table = "admin"