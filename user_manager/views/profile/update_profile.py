from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_manager.forms.updateProfile import UpdateProfileForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)

            user.save()

            messages.success(request, "Votre profil a été mis à jour avec succès!")

            if new_password:
                messages.info(request, "Votre mot de passe a été modifié. Veuillez vous reconnecter.")
                return redirect('user_manager:login')

            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user, user=request.user)

    return render(request, 'user_manager/update_profile.html', {
        'form': form
    })
