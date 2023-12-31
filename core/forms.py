from django import forms
from core.models import Contact
from django.contrib.auth.models import User
from .models import Profile,Product, AddUsers

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user','profile_pic','phone_no', 'country','studio_type','subscribed_type','business','revenue','primary_revenue']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = AddUsers
        fields = ['name', 'email', 'phone', 'profileimage', 'country']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = AddUsers
        fields = ['name', 'email', 'phone', 'profileimage', 'country']
