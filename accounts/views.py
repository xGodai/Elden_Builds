from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to 'next' parameter if provided, otherwise home
            next_url = request.POST.get(
                'next') or request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            # Form has errors, will be displayed in template
            pass
    else:
        form = CustomAuthenticationForm()  # For GET requests

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to home page after logout
    else:
        # For GET requests, redirect to home page
        return redirect('home')
