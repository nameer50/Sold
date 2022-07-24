from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    title = models.CharField(max_length=64)
    img = models.ImageField(upload_to='uploads/', blank=True, default="uploads/No_image_available.svg.png")
    discription = models.CharField(max_length=200, null="False")
    price = models.DecimalField(max_digits=19,decimal_places=2, null="False")




