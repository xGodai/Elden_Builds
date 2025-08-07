from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(
        max_length=25,
        help_text='Username must be 25 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'maxlength': '25'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter a secure password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Create user profile when user registers
            UserProfile.objects.get_or_create(user=user)
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'display_name',
            'bio',
            'profile_picture',
            'location',
            'favorite_weapon',
            'notify_on_build_like',
            'notify_on_build_comment',
            'notify_on_comment_reply',
            'notify_on_comment_vote']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your display name'
        })
        self.fields['bio'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself...'
        })
        self.fields['profile_picture'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })
        self.fields['location'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your location'
        })
        self.fields['favorite_weapon'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your favorite Elden Ring weapon'
        })

        # Notification preferences styling
        self.fields['notify_on_build_like'].widget.attrs.update(
            {'class': 'form-check-input'})
        self.fields['notify_on_build_comment'].widget.attrs.update(
            {'class': 'form-check-input'})
        self.fields['notify_on_comment_reply'].widget.attrs.update(
            {'class': 'form-check-input'})
        self.fields['notify_on_comment_vote'].widget.attrs.update(
            {'class': 'form-check-input'})
