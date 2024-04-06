from django import forms
from .models import Portfolio
from django.contrib.auth.models import User

class PortfolioForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Portfolio
        fields = ['name', 'description', 'user']