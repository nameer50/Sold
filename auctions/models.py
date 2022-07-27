from email.policy import default
from xml.parsers.expat import model
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


class Comment(models.Model):
    comment = models.TextField(blank=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="commented_on", default="1")
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_comm", default="1")

class Watchlist(models.Model):
    user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watch", default="1")
    auctions = models.ForeignKey(Auction, on_delete=models.CASCADE, default="1", related_name="listings")

class Bid(models.Model):
    Bid = models.DecimalField(decimal_places=2, max_digits=19, null='False')
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_made_by")
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_listing")

