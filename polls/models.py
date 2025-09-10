from email.policy import default
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
#import face_recognition
import numpy as np
import json
from PIL import Image
import io

# Create your models here.

class Sign(models.Model):
    name = models.CharField(max_length=25)
    perm_id = models.CharField(max_length=300, default='')
    department = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=100, default='')
    password = models.CharField(max_length=200)
    image= models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.perm_id
    
    def __str__(self) -> str:
        return self.department

    def __str__(self) -> str:
        return self.email

    def __str__(self) -> str:
        return self.password
    
    def __str__(self) -> str:
        return str(self.image)

class Log(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.username

    def __str__(self) -> str:
        return self.password
    
