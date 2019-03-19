from django import forms
from cafe.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        # include the following fields in the form.
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    is_owner = forms.BooleanField(help_text='Check if you are an owner of a cafe.', required=False)

    class Meta:
        model = UserProfile
        # include the following fields in the form.
        fields = ('is_owner',)


class CafeForm(forms.ModelForm):
    name = forms.CharField(required=True)
    pricepoint = forms.IntegerField(help_text='Enter a price average for your cafe.')
    address = forms.CharField()

    class Meta:
        model = Cafe
        # include the following fields in the form.
        fields = ('name', 'picture', 'pricepoint', 'address', 'description')


class ReviewForm(forms.ModelForm):
    CHOICES = ((1, 'Terrible'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Excellent'))
    price = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    service = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    atmosphere = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    quality = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    waiting_time = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    comments = forms.CharField(required=False)
    avg_rating = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	
    class Meta:
        model = Review
        # include all fields in the form.
        exclude = ("user", "cafe", "pub_date",)
