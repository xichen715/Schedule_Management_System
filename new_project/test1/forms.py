from django import forms
from .models import Event,Notebook


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'