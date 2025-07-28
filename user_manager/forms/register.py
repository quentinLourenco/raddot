from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'password', 'confirm_password', 'birth_date'
        ]
        labels = {
            'birth_date': 'Date de naissance'
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _("Les mots de passe ne correspondent pas."))
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_user_model()
        if user.objects.filter(email=email).exists():
            raise ValidationError("Un utilisateur avec cette adresse e-mail existe déjà.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = get_user_model()
        if user.objects.filter(username=username).exists():
            raise ValidationError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return username

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError("La date de naissance est incorrecte.")
        return birth_date
