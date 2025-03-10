from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UsersManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be provided")
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    id         = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    username   = models.CharField(max_length=50, unique=True)
    password   = models.CharField(max_length=128)
    email      = models.CharField(max_length=50)
    phone      = models.CharField(max_length=50)
    status     = models.CharField(max_length=20, default="Pending")
    interests  = models.JSONField(default=list)
    type       = models.CharField(max_length=50, default="user", choices=[('admin','Admin'), ('user','User'), ('guest','Guest')])
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)

    objects = UsersManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
