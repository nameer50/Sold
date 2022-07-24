from .models import Auction
from django.forms import ModelForm

class New_listing_form(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'discription', 'img', 'price']