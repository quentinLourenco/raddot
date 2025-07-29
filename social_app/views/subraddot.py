from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from social_app.forms.create_subraddot import CreateSubraddotForm


@login_required
def create_subraddot(request):
    if request.method == 'POST':
        form = CreateSubraddotForm(request.POST, request.FILES)
        if form.is_valid():
            subraddot = form.save(commit=False)
            subraddot.creator = request.user
            subraddot.save()

            messages.success(request, f"Le subraddot '{subraddot.name}' a été créé avec succès!")
            # return redirect('social_app:subraddot_detail', name=subraddot.name)
    else:
        form = CreateSubraddotForm()

    return render(request, 'social_app/create_subraddot.html', {
        'form': form,
        'title': 'Créer un subraddot',
    })
