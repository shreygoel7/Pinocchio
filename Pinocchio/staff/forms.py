from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class StaffSignupForm(UserCreationForm):
    """
    Form for Staff to signup for account.
    """

    dob = forms.DateField(label='Date of Birth', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1',
                  'password2')

    # Check if a user with this email already exists.
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
