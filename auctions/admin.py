from django.contrib import admin
from .models import Auction, User,Comment, Watchlist,Bid
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id","title", "img", "discription", 'price', 'user_post', 'active', 'category')
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","comment", "auction", "user_comment")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id","user_watchlist", "auctions")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user_bid", "Bid", "listing")


admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Watchlist,WatchlistAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Bid, BidAdmin)