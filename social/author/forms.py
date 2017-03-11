from django import forms

class ImageForm(forms.Form):
    forms.ImageField(label="your image")
