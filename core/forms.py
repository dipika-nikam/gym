from django import forms
from core.models import Contact
from django.contrib.auth.models import User
from .models import Profile,Product

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user','profile_pic','phone_no', 'country','studio_type','subscribed_type']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
