from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserPanel


class UserPanelForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = UserPanel
        fields = ('role', 'favoriteDoctors', 'age')
