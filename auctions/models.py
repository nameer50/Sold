from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass


class Auction(models.Model):
    title = models.CharField(max_length=64)
    img = models.ImageField(upload_to='uploads/', default="uploads/No_image_available.svg.png")
    discription = models.CharField(max_length=200, null="False")
    price = models.DecimalField(max_digits=19,decimal_places=2, null="False", validators=[MinValueValidator(limit_value=1)])
    user_post = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user", default="1")




