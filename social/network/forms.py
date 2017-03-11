from django import forms
from uploads.core.models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('description', 'document', )
