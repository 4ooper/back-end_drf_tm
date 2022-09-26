from asyncio.windows_events import NULL
from datetime import date
import datetime
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

from .managers import CustomUserManager

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.TextField()
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name

class CardStyles(models.Model):
    name = models.TextField()
    color = models.TextField()
    pictureURL = models.ImageField(upload_to="photos/cardStyles/")

    def __str__(self):
        return self.name

class Laboratories(models.Model):
    name = models.TextField()
    count = models.IntegerField()
    deadline = models.DateField()
    ready = models.IntegerField(default=0)

class Relations(models.Model):
    styleID = models.ForeignKey('CardStyles', on_delete=models.CASCADE)
    userID = models.ForeignKey('User', on_delete=models.CASCADE)
    labID = models.ForeignKey('Laboratories', on_delete=models.CASCADE, default=0)

class ReadyTasks(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    lab = models.ForeignKey('Laboratories', on_delete=models.CASCADE)
    ready_task = models.IntegerField()
    ready_date = models.DateField(default=date.today)