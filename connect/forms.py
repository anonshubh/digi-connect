from django import forms

from .models import Request

class RequestForm(forms.ModelForm):
    genre = forms.ChoiceField()
    class Meta:
        model = Request
        exclude = ('requester','genre','is_first_year_req',)
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control-sm'}),
            'content':forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }
