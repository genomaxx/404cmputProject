from django.contrib.auth.models import User
from django import forms
from author.models import Author

class EditForm(forms.ModelForm):

    class Meta:
        model = Author
        # Note: The name for the inputs on the HTML page MUST match the name of the fields
        fields = ['firstname', 'lastname', 'phone', 'dob', 'gender', 'gitURL']
