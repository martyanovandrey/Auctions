from django.contrib import admin
from . models import Listing, Comment, User, Watchlist
# Register your models here.

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Watchlist)