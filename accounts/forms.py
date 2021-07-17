from django import forms
from django.contrib.auth.models import User
from .models import Tenant, Owner
from django.contrib import messages

User_types = (
    ("Tenant", "Tenant"),
    ("PG Owner", "PG Owner"),
    ("Admin", "Admin"),
)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username : ")
    password = forms.CharField(label="Password : ", widget=forms.PasswordInput)
    user_type = forms.ChoiceField(label="User Type : ", choices=User_types)

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="Password : ", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password : ", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Username : ',
            'first_name': 'First Name : ',
            'last_name': 'Last Name : ',
            'email': 'Email : ',
        }