from django import forms

from .models import Request

class RequestForm(forms.ModelForm):
    genre = forms.ChoiceField()
    class Meta:
        model = Request
        exclude = ('genre',)
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control-sm'})
        }
