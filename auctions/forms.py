
from .models import Auction, Comment
from django.forms import ModelForm

class New_listing_form(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'discription', 'img', 'price']

class New_Comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']