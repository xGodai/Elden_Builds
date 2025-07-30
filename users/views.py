from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('build-list')  # Redirect to the build list after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})
