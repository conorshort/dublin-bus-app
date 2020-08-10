from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
import datetime  # for checking date range.
# from crispy_forms.helper import FormHelper


class leapCardForm(forms.Form):
    # helper = FormHelper()

    username = forms.CharField(widget= forms.TextInput(attrs={'id':'un','style':'margin-right: 30%;margin-left: 2%'}))

    password = forms.CharField(widget=widgets.PasswordInput(attrs={'id':'pw','style':'margin: 3%;'}))
    # remember_me = forms.BooleanField(required=False)


# class JourneyPlannerForm(forms.Form):
#     from_location = forms.CharField()
#     to_location = forms.CharField()
#     date = forms.DateField(help_text="Enter a date between now and 1 week.")
#     time = forms.TimeField()

#     def clean_date(self):
#         data = self.cleaned_data['date']
#         #Check date is not in past.
#         if data < datetime.date.today():
#             raise ValidationError('Invalid date - daye in past')

#         #Check date is in range within 1 week.
#         if data > datetime.date.today() + datetime.timedelta(weeks=1):
#             raise ValidationError('Invalid date - date more than 1 week ahead')

#         # Remember to always return the cleaned data.
#         return data
