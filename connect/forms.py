from django import forms
from django.core.exceptions import ValidationError

from .models import Request


class RequestForm(forms.ModelForm):
    genre_list = forms.ChoiceField()
    class Meta:
        model = Request
        exclude = ('requester','genre','is_first_year_req',)
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control-sm'}),
            'content':forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }