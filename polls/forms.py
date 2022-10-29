from logging import PlaceHolder
from django import forms
from polls.models import Sign

class SignForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label="")
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="")

    class Meta():
        model = Sign
        fields = ["username","email", "password"]
        
class LogForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="")
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="")

    class Meta():
        model = Sign
        fields = ["username","password"]