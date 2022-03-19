from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length = 32)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    img_url = models.URLField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="listing")
    active = models.BooleanField(default=False)
    watchlist=models.ManyToManyField(User, blank=True, related_name="listing_on_watchlist")
    time = models.DateTimeField(default=datetime.datetime.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=3)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")
    listing = models.ForeignKey(Listing,null=True, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Value:{self.value}, On {self.listing}, By {self.bid_user}"

class Comment(models.Model):
    content = models.CharField(max_length=100)
    time = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_written")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment: '{self.content}' by '{self.author}' at {self.time} on {self.listing}"
