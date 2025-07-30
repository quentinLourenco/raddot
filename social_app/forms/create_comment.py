from django import forms
from social_app.models.Comment import Comment

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Ajouter un commentaire...',
                'rows': 2,
                'class': 'create-comment-textarea',
            }),
        }
        labels = {
            'content': '',
        }

