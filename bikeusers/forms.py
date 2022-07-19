from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from bikeusers.token import token_generator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from bikeusers.models import Bikes,BikeImages

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class': '  form-control form-control-user'}))
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class': '  form-control form-control-user'}))
    class Meta:
        model=User
        fields= ['first_name','last_name','email','username','password1','password2']
        widgets={

            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
             }

        # We need the user object, so it's an additional parameter
    def send_activation_email(self, request, user):
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string(
                'activate_account.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }
            )

            user.email_user(subject, message, html_message=message)

class LoginForm(forms.Form):
    username = forms.CharField(label='Email or Username',widget=forms.TextInput(attrs={'class': '  form-control form-control-user'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': '  form-control form-control-user'}))


class PostBikeForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))
    class Meta:
        model= Bikes
        exclude = ('added_user', 'date', 'active_status',)
        widgets= {
            'bike_name': forms.TextInput(attrs={'class':' form-control form-control-user','placeholder':'Bikename'}),
            'bike_manufacturer': forms.TextInput(attrs={'class':' form-control form-control-user','placeholder':'Manufacturer'}),
            'bike_model':forms.NumberInput(attrs={'class':' form-control form-control-user','placeholder':'Model'}),
            'bike_km': forms.NumberInput(attrs={'class': ' form-control form-control-user', 'placeholder': 'KilometerDriven'}),
            'bike_price':forms.NumberInput(attrs={'class':' form-control form-control-user','placeholder':'Price'}),
            'image':forms.ClearableFileInput(attrs={'class':' form-control form-control-user','placeholder':'image'}),
            'bike_capacity':forms.NumberInput(attrs={'class':' form-control form-control-user','placeholder':'CubicCapacity'}),
            'bike_description':forms.Textarea(attrs={'class':' form-control form-control-user','placeholder':'Description'}),
            'owner_type':forms.Select(attrs={'class':' form-control form-control-user '}),
            'address':forms.TextInput(attrs={'class':' form-control form-control-user','placeholder':'Communication Address'}),


        }
# class BikeImageForm(forms.ModelForm):
#     class Meta:
#         model= BikeImages
#         fields=('bike_images',)
#         widgets={
#             'bike_images':forms.ClearableFileInput(attrs={'multiple': True})
#         }


