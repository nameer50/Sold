from django.contrib import admin
from .models import Auction, User,Comment
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","comment", "auction", "user_comment")

admin.site.register(User, UserAdmin)
admin.site.register(Auction)
admin.site.register(Comment,CommentAdmin)