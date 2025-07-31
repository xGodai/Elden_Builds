from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Write your comment here...',
            'class': 'form-control'
        }),
        label='Comment'
    )

    class Meta:
        model = Comment
        fields = ['content']
