from django import forms
from core.models import Contact
from django.contrib.auth.models import User
from .models import Profile,Product, AddUsers, Lead, StaffMember

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
        fields = ['name', 'email', 'phone', 'profile', 'assigned_to', 'refered_by']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = AddUsers
        fields = ['name', 'email', 'phone', 'profile', 'assigned_to', 'refered_by']

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['status', 'email', 'name', 'birthday', 'postal_code', 'mobile_no', 'objectives', 'refered_by', 'notes']

class UpdateLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['status', 'email', 'name', 'birthday', 'postal_code', 'mobile_no', 'objectives', 'refered_by', 'notes']

class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ['fullname', 'email', 'address', 'postal_code', 'phone_no', 'gender']

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ['fullname', 'email', 'address', 'postal_code', 'phone_no', 'gender']
