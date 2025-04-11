from django import forms
from .models import DigitalContent

class DigitalContentForm(forms.ModelForm):
    class Meta:
        model = DigitalContent
        fields = ['name', 'description', 'access_by', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
