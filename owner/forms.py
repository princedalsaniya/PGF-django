from django import forms
from django.contrib.auth.models import User
from accounts.models import Owner, Tenant
from .models import pgDetails, pgFacilities, roomDetails, pgPhotos, pgRules, ratings, messages, applicationDetails

pgTypes = (
    ('Boys', "Only Boys"),
    ('Girls', "Only Girls"),
    ('Both', "Both"),
)

class register_new_pg_form(forms.ModelForm):
    type = forms.ChoiceField(label="Select type of your PG : ", choices=pgTypes)
    floors = forms.IntegerField(label="Number of Floors : ", min_value=1)
    rooms = forms.IntegerField(label="Number of Rooms : ", min_value=0)
    total_intakes = forms.IntegerField(label="No of Total intakes : ", min_value=1)
    available_intakes = forms.IntegerField(label='No of Available intakes : ', min_value=0)
    start_rent = forms.IntegerField(label='Lowest Rent : ', min_value=0)
    end_rent = forms.IntegerField(label='Highest Rent : ', min_value=0)

    class Meta:
        model = pgDetails
        fields = ('floors', 'rooms', 'name', 'address', 'area', 'city', 'state', 'total_intakes', 'available_intakes', 'description', 'start_rent', 'end_rent')
        labels = {
            'name': 'Name of your PG : ',
            'address': 'Address : ',
            'area': 'Area : ',
            'city': 'City : ',
            'state': 'State : ',
            'description': 'Description : ',
        }

class register_facilities_form(forms.ModelForm):
    class Meta:
        model = pgFacilities
        fields = ('ac', 'balcony', 'laundry', 'breakfast', 'lunch', 'dinner', 'parking', 'cleaning', 'wifi', 'tv', 'fridge', 'ro', 'gym', 'lift', 'generator')
        labels = {
            'ac': 'do have AC : ',
            'balcony': 'do have Balconny : ',
            'laundry': 'do have Laundry : ',
            'breakfast': 'do give BreakFast : ',
            'lunch': 'do give Lunch : ',
            'dinner': 'do give Dinner : ',
            'parking': 'do have Parking : ',
            'cleaning': 'do provide Cleaning : ',
            'wifi': 'do have WiFi : ',
            'tv': 'do have TV : ',
            'fridge': 'do have Fridge : ',
            'ro': 'do have water R/O : ',
            'gym': 'do have Gym : ',
            'lift': 'do have Lift : ',
            'generator': 'do have Generator : ',
        }

class register_rules_form(forms.ModelForm):
    deposit = forms.IntegerField(label="Deposit Amount : ", min_value=0)
    class Meta:
        model = pgRules
        fields = ('deposit', 'haveClosingTime', 'visitors', 'nonVeg', 'oppositeGender', 'smoking', 'drinking', 'loudMusic', 'party')
        labels = {
            'haveClosingTime': 'Any time-limit for allowed entry in PG : ',
            'visitors': 'Visitors Allowed : ',
            'nonVeg': 'Non Veg food Allowed : ',
            'oppositeGender': 'Opposite Gender Entry Allowed : ',
            'smoking': 'Smoking Allowed : ',
            'drinking': 'Drinking Allowed : ',
            'loudMusic': 'Loud Music Allowed : ',
            'party': 'Parties Allowed : ',
        }

class register_photo_form(forms.ModelForm):
    # photoPID = forms.CharField(label="",max_length=20)
    # photoPID.widget.attrs.update({'style': 'display:none'})

    class Meta:
        model = pgPhotos
        fields = ('message',)
        labels = {
            'message': 'Description of Photo : '
        }
