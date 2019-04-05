from django import forms
import re
from django.core.exceptions import ValidationError




class SearchCompanyForm(forms.Form):
    # captcha = NoReCaptchaField()
    tickerSymbol = forms.CharField(label='', widget=forms.TextInput(attrs={'autofocus': 'autofocus','size':25, 'maxlength':25,
                        'style': 'font: Agency FB, font-size: x-large', 'placeholder': 'Enter CUSIP', 'text-align': 'center'}))
    def clean(self):
        unvalidated_data = super(SearchCompanyForm, self).clean()
        cleaned_data = unvalidated_data.get('tickerSymbol')
        # dirt = re.findall(r'[@#$%\^&*\(\)\{\}\[\|\/!~\_\]?<>\.-]', tickerSymbol)
        # if dirt == []:
        #     cleaned_data = unvalidated_data
        # else:
        #     raise ValidationError("Invalid characters in the keyword '%s'" % tickerSymbol)
class FindCusipForm(forms.Form):
    # captcha = NoReCaptchaField()
    cusip = forms.CharField(label='', widget=forms.TextInput(attrs={'autofocus': 'autofocus','size':25, 'maxlength':25,
                        'style': 'font: Agency FB, font-size: x-large', 'placeholder': 'Enter a search term', 'text-align': 'center'}))
    def clean(self):
        unvalidated_data = super(FindCusipForm, self).clean()
        cleaned_data = unvalidated_data.get('tickerSymbol')
