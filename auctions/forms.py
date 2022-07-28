
from .models import Auction, Comment, Bid
from django.forms import ModelForm

class New_listing_form(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'discription', 'img', 'price', 'category']


class New_Comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class New_Bid_form(ModelForm):
    class Meta:
        model = Bid
        fields = ['Bid']
