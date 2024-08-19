from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class PlayerForm(ModelForm):
	class Meta:
		model = Player
		fields = '__all__'
  
class CoachForm(ModelForm):
	class Meta:
		model = Coach
		fields = '__all__'

class MatchForm(ModelForm):
	class Meta:
		model = UpcomingMatches
		fields = '__all__'

class PlayerCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
