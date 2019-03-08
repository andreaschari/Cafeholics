from django import forms
from django.contrib.auth.models import User
from cafe.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        # include the following fields in the form.
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    is_owner = forms.BooleanField(help_text='Check if you are an owner of a cafe.')

    class Meta:
        model = UserProfile
        # include the following fields in the form.
        fields = ('is_owner',)


class CafeForm(forms.ModelForm):
    # the owner is input by the view
    # owner = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(required=True)
    # picture = forms.ImageField(upload_to='cafe_images', required=False)
    pricepoint = forms.IntegerField(help_text='Enter a price average for your cafe.')
    # slug = models.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Cafe
        # include the following fields in the form.
        fields = ('name', 'picture', 'pricepoint', 'description')


class ReviewForm(forms.ModelForm):
    price = forms.IntegerField(help_text='Enter a value from 1 out of 5')
    service = forms.IntegerField(help_text='Enter a value from 1 out of 5')
    atmosphere = forms.IntegerField(help_text='Enter a value from 1 out of 5')
    quality = forms.IntegerField(help_text='Enter a value from 1 out of 5')
    waiting_time = forms.IntegerField(help_text='Enter a value from 1 out of 5')
    comments = forms.CharField(required=False)

    class Meta:
        model = Review
        # include all fields in the form.
        fields = '__all__'
