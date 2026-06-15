from django import forms
from .models import Dataset


class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Ventes 2024, Dataset Iris…',
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv',
            }),
        }
        labels = {
            'name': 'Nom du dataset',
            'file': 'Fichier CSV',
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith('.csv'):
                raise forms.ValidationError('Seuls les fichiers .csv sont acceptés.')
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('Le fichier ne doit pas dépasser 50 Mo.')
        return file
