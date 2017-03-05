from django.contrib.auth.models import User
from django import forms

'''
Follow this documentation as a reference
https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/

Using ModelForm to save passwords:
http://stackoverflow.com/questions/2936276/django-modelforms-user-and-userprofile-not-hashing-password

Since we are mapping our form input to Models, we should be using ModelForm instead of Form.
'''
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='reg_password', widget=forms.PasswordInput())

    class Meta:
        model = User
        # Note: The name for the inputs on the HTML page MUST patch the name of the fields for creating new Users
        fields = ['username', 'email', 'password']
    
    '''
    Old code.  Keeping for now as reference in the future if needed

    userName = forms.CharField(label="reg_username", max_length="32")
    email = forms.EmailField(label="reg_email")
    password = forms.CharField(label="reg_password", widget=forms.PasswordInput)
    '''