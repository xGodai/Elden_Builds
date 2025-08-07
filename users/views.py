from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import DetailView
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile
from builds.models import Build, Comment

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}! You can now log in.')
            login(request, user)  # Automatically log in the user
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_edit(request):
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('user-profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_edit.html', context)


class UserProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Get or create user profile
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        context['user_profile'] = user_profile

        # Get user's builds
        user_builds = Build.objects.filter(user=user).order_by('-created_at')

        # Get user's liked builds
        liked_builds = Build.objects.filter(
            liked_by=user).order_by('-created_at')

        # Get user's comments
        user_comments = Comment.objects.filter(
            user=user).select_related('build').order_by('-created_at')

        # Get current tab from URL parameters
        current_tab = self.request.GET.get('tab', 'builds')

        context.update({
            'user_builds': user_builds,
            'liked_builds': liked_builds,
            'user_comments': user_comments,
            'current_tab': current_tab,
            'is_own_profile': self.request.user == user,
        })

        return context


@login_required
def my_profile(request):
    """Redirect to the current user's profile"""
    return redirect('user-profile', username=request.user.username)
