from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from user_manager.forms.login import LoginForm
from user_manager.models import User


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)

                # if group == 'JobSeeker':
                #     try:
                #         JobSeeker.objects.get(user=user)
                #         return redirect('job_finder:dashboard')
                #     except JobSeeker.DoesNotExist:
                #         messages.info(request, "Veuillez compléter votre profil de demandeur d'emploi.")
                #         return redirect('register_jobseeker')

                return redirect('social_app:homepage')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'user_manager/login.html', {'form': form})
