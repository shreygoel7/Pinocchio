from django import forms

class LoginForm(forms.Form):
    """
    Login form for users.
    """

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
