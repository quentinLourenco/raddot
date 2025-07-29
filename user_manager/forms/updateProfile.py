from django import forms
from user_manager.models.User import User
from django.contrib.auth.password_validation import validate_password

class UpdateProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    new_password = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    confirm_new_password = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.user.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username != self.user.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        password_fields_modified = new_password or self.has_changed()

        if password_fields_modified:
            if not current_password:
                self.add_error('current_password', "Veuillez entrer votre mot de passe actuel pour confirmer les modifications.")
            elif not self.user.check_password(current_password):
                self.add_error('current_password', "Mot de passe incorrect.")

        if new_password:
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', "Les mots de passe ne correspondent pas.")
            else:
                try:
                    validate_password(new_password, self.user)
                except forms.ValidationError as error:
                    self.add_error('new_password', error)

        return cleaned_data
