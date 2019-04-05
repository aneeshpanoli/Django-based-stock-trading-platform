from django import forms
import re
from django.core.exceptions import ValidationError




class SubmitTickerSymbolForm(forms.Form):
    # captcha = NoReCaptchaField()
    tickerSymbol = forms.CharField(label='', widget=forms.TextInput(attrs={'autofocus': 'autofocus','size':8, 'maxlength':5,
                        'style': 'font: Agency FB, font-size: x-large', 'placeholder': 'Enter a ticker', 'text-align': 'center'}))
    def clean(self):
        unvalidated_data = super(SubmitTickerSymbolForm, self).clean()
        cleaned_data = unvalidated_data.get('tickerSymbol')
        # dirt = re.findall(r'[@#$%\^&*\(\)\{\}\[\|\/!~\_\]?<>\.-]', tickerSymbol)
        # if dirt == []:
        #     cleaned_data = unvalidated_data
        # else:
        #     raise ValidationError("Invalid characters in the keyword '%s'" % tickerSymbol)
