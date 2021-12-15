from django.contrib import admin
from .models import Categories, Auctions, Comments, Bid, User, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Auctions)
admin.site.register(Comments)
admin.site.register(Bid)
admin.site.register(Watchlist)