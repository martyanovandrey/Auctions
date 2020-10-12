from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    description = models.CharField(max_length=254)
    url = models.CharField(max_length=254)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.price} {self.description} {self.url} {self.date}"    

class Watchlist(models.Model):
    user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
    listing_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_item')
    def __str__(self):
        return f"{self.user_watchlist} {self.listing_item}"

    def is_added(self):
        return

class Comment(models.Model):
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=1024)
    date = models.DateTimeField()    

    def __str__(self):
        return f"{self.name} ({self.comment}) {self.date}"      
