from django import forms
from django.forms import inlineformset_factory
from .models import Build, BuildImage, Comment


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ['title', 'description', 'weapons', 'armor', 'talismans', 'spells', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter build title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your build...'
            }),
            'weapons': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'List your weapons'
            }),
            'armor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'List your armor sets'
            }),
            'talismans': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'List your talismans'
            }),
            'spells': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'List your spells (optional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class BuildImageForm(forms.ModelForm):
    class Meta:
        model = BuildImage
        fields = ['image', 'is_primary', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional image caption'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (10MB limit)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Image file too large. Maximum size is 10MB.')
            
            # Check file format
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('File must be an image.')
        
        return image


# Formset for handling multiple images
BuildImageFormSet = inlineformset_factory(
    Build, 
    BuildImage, 
    form=BuildImageForm,
    extra=1,
    max_num=3,
    min_num=0,
    can_delete=True,
    fields=['image', 'is_primary', 'caption']
)


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
