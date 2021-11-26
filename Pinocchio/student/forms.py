from academicInfo.models import Department

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class StudentSignupForm(UserCreationForm):
    """
    Form for Student to signup for account.
    """

    batch = forms.IntegerField(required=True,
                               validators=[MinValueValidator(2000), MaxValueValidator(9999)]
                               )
    dob = forms.DateField(label='Date of Birth', required=True)
    department = forms.ModelChoiceField(label='Department',
                                        queryset=Department.objects.all(),
                                        empty_label=None)

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
        self.fields['username'].label = 'Roll number'
        self.fields['email'].label = 'Email'
        self.fields['batch'].label = 'Batch'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
