from cgi import print_exception
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"


class Courier(models.Model):
    courier = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/', null= True, blank= True)  
