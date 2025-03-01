from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']  # Only take the file input
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
