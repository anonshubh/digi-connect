from allauth.account.forms import SignupForm , LoginForm
from django import forms
from allauth.account.adapter import DefaultAccountAdapter 
from django.forms import ValidationError

from .models import UserInfo


class CustomLoginForm(LoginForm):
     def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs = {'placeholder': 'Handle or Institute Email', 'autofocus': 'autofocus'}


class CustomSignupForm(SignupForm):
    """
    Custom SignUp Form and Also Created New user_info Object
    """

    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    DEPARTMENT_YEAR = [
        ('1btech', 'BTech - 1th Year'),
        ('2btech', 'BTech - 2th Year'),
        ('3btech', 'BTech - 3th Year'),
        ('4btech', 'BTech - 4th Year'),
        ('5btech', 'BTech - 5th Year'),
        ('mtech', 'MTech'),
        ('phd', 'PhD'),
        ('faculty', 'Faculty'),
    ]

    first_name = forms.CharField(max_length=30, label='First Name') 
    last_name = forms.CharField(max_length=30, label='Last Name')
    age = forms.IntegerField(label='Age')
    gender = forms.ChoiceField(choices=GENDER,label='Gender')
    phone = forms.IntegerField(label='Phone Number')
    department_year = forms.ChoiceField(choices=DEPARTMENT_YEAR,label='Department And Year')


    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name'] 
        user.last_name = self.cleaned_data['last_name']
        user.save()

        age = self.cleaned_data['age']
        gender = self.cleaned_data['gender']
        phone = self.cleaned_data['phone']
        department_year = self.cleaned_data['department_year']

        year = 0
        department = ""

        if (department_year != 'mtech') and (department_year != 'phd') and (department_year != 'faculty'):
            year = int(department_year[0])
            department = department_year[1:]
        else:
            department = department_year

        user_info , created = UserInfo.objects.get_or_create(
            user=user,
            age = age,
            gender = gender,
            phone = phone,
            department = department,
            year = year
        )

        return user


class RestrictEmailAdapter(DefaultAccountAdapter): 
    """
    Verifies Authorization of Email
    """
    def clean_email(self, email): 
        email = email.lower()

        RestrictedList = [] # List will include Restricted Emails 
        if email in RestrictedList: 
            raise ValidationError('You are Restricted from Registering!')

        index = email.find('@')
        dot = email.find('.')

        domain = email[index+1:dot]

        if(domain=='gmail'):
            raise ValidationError("Use only Official Institute Email ID!")

        if(email[index+1:]!='iiitdm.ac.in'):
            raise ValidationError("Re-Check Email Address!")

        return email