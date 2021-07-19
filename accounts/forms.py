from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput

from .models import Tenant, Owner
from django.contrib import messages

User_types = (
    ("Tenant", "Tenant"),
    ("Owner", "PG Owner"),
    ("Admin", "Admin"),
)
Signup_user_types = (
    ("Tenant", "Tenant"),
    ("Owner", "PG Owner"),
)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username : ")
    password = forms.CharField(label="Password : ", widget=forms.PasswordInput)
    user_type = forms.ChoiceField(label="User Type : ", choices=User_types)

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="Password : ", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password : ", widget=forms.PasswordInput)
    type = forms.ChoiceField(label="Select your Type : ", choices=Signup_user_types)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Username : ',
            'first_name': 'First Name : ',
            'last_name': 'Last Name : ',
            'email': 'Email : ',
        }

class createTenantProfileForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ('phone', 'workplace', 'adharNo', 'bdate')
        labels = {
            'phone': 'Mobile Number : ',
            'workplace': 'Workplace/Studyplace : ',
            'adharNo': "Aadhar Number : ",
            'bdate': "Birthdate : ",
        }
        placeholders = {
            'phone': 'Enter your mobile number...',
            'workplace': "Enter where work or study...",
            'adharNo': "Enter youe Aadhar Number...",
        }
        widgets = {
            'bdate': DateInput(attrs={'type': 'date'}),
        }