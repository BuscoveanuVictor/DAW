from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm

def register_view(request):
    if request.method == 'POST':
        pass
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            # return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(86400)  # 24 ore în secunde
                else:
                    request.session.set_expiry(0)
                return redirect('profile')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})