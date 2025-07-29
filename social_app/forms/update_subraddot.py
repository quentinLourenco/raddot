from django import forms
from social_app.models.Subraddot import Subraddot

class UpdateSubraddotForm(forms.ModelForm):
    class Meta:
        model = Subraddot
        fields = ['description', 'banner', 'icon']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de la communauté',
                'rows': 5
            }),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Description',
            'banner': 'Bannière (optionnel)',
            'icon': 'Icône (optionnel)',
        }
        help_texts = {
            'description': 'Décrivez l\'objectif de votre communauté.',
            'banner': 'Taille recommandée : 1200×400 pixels',
            'icon': 'Format carré recommandé, 200×200 pixels',
        }
