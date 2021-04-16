from django import forms
from django.forms import ModelForm
from .models import User, Category, Club, Field, Booking, Schedule



class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['club', 'address', 'address_number', 'city', 'zip_code', 'country', 'image_url']
        widgets = {"club": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name of the club'}),
                    'image_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'url of the image of the club'}),
                    "address": forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Address of the club'}),
                    "address_number": forms.NumberInput(attrs={'class': 'form-control' }),
                    "city": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City of the club'}),
                    "zip_code": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code of the club'}),
                    "country": forms.Select(attrs={'class' : 'form-control'}),
        }
      

class FieldForm(ModelForm):
    class Meta:
        model = Field
        fields = ['field_name', 'category', 'price', 'address', 'address_number', 'city', 'zip_code', 'country']
        widgets = {"field_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the field'}),
                    'price': forms.NumberInput(attrs={'class': 'form-control' }),
                    "address": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address of the field'}),
                    "address_number": forms.NumberInput(attrs={'class': 'form-control' }),
                    "city": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City of the field'}),
                    "zip_code": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code of the field'}),
                    "country": forms.Select(attrs={'class' : 'form-control'}),
        }
