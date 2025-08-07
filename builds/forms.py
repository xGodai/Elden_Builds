from django import forms
from django.forms import inlineformset_factory
from .models import Build, BuildImage, Comment


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = [
            'title',
            'description',
            'weapons',
            'armor',
            'talismans',
            'spells',
            'category',
            'level',
            'vigor',
            'mind',
            'endurance',
            'strength',
            'dexterity',
            'intelligence',
            'faith',
            'arcane']
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
            }),
            # Player Stats
            'level': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Character level',
                'min': '1',
                'max': '713'
            }),
            'vigor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vigor',
                'min': '1',
                'max': '99'
            }),
            'mind': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mind',
                'min': '1',
                'max': '99'
            }),
            'endurance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endurance',
                'min': '1',
                'max': '99'
            }),
            'strength': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Strength',
                'min': '1',
                'max': '99'
            }),
            'dexterity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dexterity',
                'min': '1',
                'max': '99'
            }),
            'intelligence': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Intelligence',
                'min': '1',
                'max': '99'
            }),
            'faith': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Faith',
                'min': '1',
                'max': '99'
            }),
            'arcane': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Arcane',
                'min': '1',
                'max': '99'
            })
        }


class BuildImageForm(forms.ModelForm):
    class Meta:
        model = BuildImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_primary': forms.HiddenInput()  # Hidden field, managed automatically
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Only validate size and type for new uploads, not existing CloudinaryResource
            if hasattr(image, 'size') and hasattr(image, 'content_type'):
                # Check file size (10MB limit)
                if image.size > 10 * 1024 * 1024:
                    raise forms.ValidationError(
                        'Image file too large. Maximum size is 10MB.')

                # Check file format
                if not image.content_type.startswith('image/'):
                    raise forms.ValidationError('File must be an image.')

        return image


# Custom formset class for additional validation
class BaseBuildImageFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """Ensure max 3 images and first image is primary"""
        if any(self.errors):
            return
        
        valid_forms = []
        
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                valid_forms.append(form)
        
        # Ensure max 3 images
        if len(valid_forms) > 3:
            raise forms.ValidationError(
                'You can upload a maximum of 3 images.'
            )
        
        # Automatically set first image as primary
        if valid_forms:
            # Reset all primary flags
            for form in valid_forms:
                form.cleaned_data['is_primary'] = False
            # Set first image as primary
            valid_forms[0].cleaned_data['is_primary'] = True


# Formset for handling multiple images
BuildImageFormSet = inlineformset_factory(
    Build,
    BuildImage,
    form=BuildImageForm,
    formset=BaseBuildImageFormSet,
    extra=1,  # Start with 1 empty form
    max_num=3,
    min_num=0,
    can_delete=True,
    validate_max=True,
    fields=['image', 'is_primary']  # Removed caption
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
