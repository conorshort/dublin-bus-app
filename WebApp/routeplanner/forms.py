from django import forms
from django.forms import widgets
# from crispy_forms.helper import FormHelper

class leapCardForm(forms.Form):
    # helper = FormHelper()
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput)
    # remember_me = forms.BooleanField(required=False)