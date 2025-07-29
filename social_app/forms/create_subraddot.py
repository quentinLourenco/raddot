from django import forms
from social_app.models.Subraddot import Subraddot

class CreateSubraddotForm(forms.ModelForm):
    class Meta:
        model = Subraddot
        fields = ['name', 'description', 'banner', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du subraddot'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du subraddot',
                'rows': 5
            }),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nom du subraddot',
            'description': 'Description',
            'banner': 'Bannière (optionnel)',
            'icon': 'Icône (optionnel)',
        }
        help_texts = {
            'name': 'Choisissez un nom unique pour votre subraddot. Vous ne pourrez pas le modifier ultérieurement.',
            'description': 'Décrivez l\'objectif de votre subraddot.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            import re
            if not re.match('^[a-zA-Z0-9_-]+$', name):
                raise forms.ValidationError(
                    "Le nom du subraddot ne peut contenir que des lettres, des chiffres, des tirets et des underscores."
                )
        return name
