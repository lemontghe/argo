from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile, AdsPlan
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter a username'}), help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter your email', "type": "email"}), help_text="Enter a valid email.")
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length= 25, label='',  widget=forms.TextInput(attrs={'placeholder': 'Enter a username', "class": "form-control"}))
    password = forms.CharField(max_length= 30, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password', "class": "form-control"}))


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': u'Enter your old password', "class": "form-control", "type": "password", "id": "new", "name": "new", "required": ""}))
    new_password1 = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': u'Enter a new password', "class": "form-control", "type": "password", "id": "new", "name": "new", "required": ""}))
    new_password2 = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': u'Confirm your new password', "class": "form-control", "type": "password", "id": "new", "name": "new", "required": ""}))


class PasswordResetingForm(PasswordResetForm):
    email = forms.EmailField(min_length=5, label='', widget=forms.TextInput(attrs={"class": "form-control", "id": '', "name": "rec_email", "placeholder": "Enter your email",  "type": "email", "required": ""}))


class PaymentForm(forms.ModelForm):
    payeer = forms.CharField(max_length=9, min_length=9, required=0, label='', widget=forms.TextInput(attrs={'placeholder': 'For example: P12345678', "class": "form-control", "type": "text", "id": "pursepy", "name": "purse"}))
    perfectmoney = forms.CharField(max_length=9, min_length=9, required=0, label='', widget=forms.TextInput(attrs={'placeholder': 'For example: U12345678', "class": "form-control", "type": "text", "id": "pursepm", "name": "purse"}))
    class Meta:
        model = Profile
        fields = ("payeer", "perfectmoney")


class AddSurfForm(forms.ModelForm):
    title = forms.CharField(max_length=70, min_length=7, widget=forms.TextInput(attrs={'placeholder': 'For example: Great site, watch everyone!', "class": "form-control", "type": "text", "id": "addsurfTitle"}))
    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'For example: https://google.com', "class": "form-control", "type": "url"}))
    class Meta:
        model = Profile
        fields = ("title", "url")


class EditSiteForm(forms.ModelForm):
    title = forms.CharField(max_length=70, min_length=7, widget=forms.TextInput(attrs={'placeholder': 'For example: Great site, watch everyone!', "class": "form-control", "type": "text"}))
    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'For example: https://google.com', "class": "form-control", "type": "url"}))
    ads = AdsPlan.objects.all()
    ch = [(ad.id, ad.name) for ad in ads]
    no_plan = forms.ChoiceField(required=False, choices=tuple(ch), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ("title", "url", "no_plan")


class SiteBalanceForm(forms.ModelForm):
    coin = forms.CharField(max_length=7, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter coins', "class": "form-control form-control-alternative", "type": "number",  "step": "any", "autocomplete": "off", "id": "coin_input", "min": "0"}))
    class Meta:
        model = Profile
        fields = ("coin", )
