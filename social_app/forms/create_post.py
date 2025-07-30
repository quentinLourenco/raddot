from django import forms
from social_app.models.Post import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post_type', 'content', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre de votre post', 'required': True}),
            'content': forms.Textarea(attrs={'placeholder': 'Contenu de votre post'}),
            'img': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
