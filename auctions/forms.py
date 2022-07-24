from django import forms

class New_listing_form(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    discription = forms.CharField(label="Discription", max_length=500)
    cost = forms.DecimalField(label="Starting bid", decimal_places=2, max_digits=19, min_value=1)
    img = forms.ImageField(required=False)