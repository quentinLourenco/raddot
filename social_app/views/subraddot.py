from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from social_app.toaster import notify

from social_app.forms.create_subraddot import CreateSubraddotForm
from social_app.models.Subraddot import Subraddot
from social_app.forms.update_subraddot import UpdateSubraddotForm
from social_app.models.Post import Post


def subraddot_create(request):
    if request.method == 'POST':
        form = CreateSubraddotForm(request.POST, request.FILES)
        if form.is_valid():
            subraddot = form.save(commit=False)
            subraddot.creator = request.user
            subraddot.save()
            subraddot.members.add(request.user)

            notify(request, "success", f"Le subraddot '{subraddot.name}' a été créé avec succès!")
            # return redirect('social_app:subraddot_detail', name=subraddot.name)
    else:
        form = CreateSubraddotForm()

    return render(request, 'social_app/subraddot_create.html', {
        'form': form,
        'title': 'Créer un subraddot',
    })


def subraddot_update(request, name):
    subraddot = get_object_or_404(Subraddot, name=name)

    # Vérifier que l'utilisateur est bien le créateur
    if subraddot.creator != request.user:
        raise Http404("Vous n'êtes pas autorisé à modifier cette communauté")

    if request.method == 'POST':
        form = UpdateSubraddotForm(request.POST, request.FILES, instance=subraddot)
        if form.is_valid():
            form.save()
            notify(request, "success", f"La communauté r/{subraddot.name} a été mise à jour avec succès!")
            return redirect('social_app:my_subraddots')
    else:
        form = UpdateSubraddotForm(instance=subraddot)

    return render(request, 'social_app/subraddot_update.html', {
        'form': form,
        'subraddot': subraddot
    })


def subraddot_home(request, name):
    subraddot = get_object_or_404(Subraddot, name=name)
    posts = Post.objects.filter(subraddot=subraddot).order_by('-created_at')

    context = {
        'subraddot': subraddot,
        'posts': posts,
        'is_member': request.user in subraddot.members.all() if request.user.is_authenticated else False
    }

    return render(request, 'social_app/subraddot_home.html', context)


@login_required
def join_subraddot(request, name):
    if request.method == 'POST':
        subraddot = get_object_or_404(Subraddot, name=name)

        # Vérifier si l'utilisateur est déjà membre
        if request.user in subraddot.members.all():
            notify(request, "info", f"Vous êtes déjà membre de r/{subraddot.name}")
        else:
            subraddot.members.add(request.user)
            notify(request, "success", f"Vous avez rejoint r/{subraddot.name} avec succès!")

        # Redirection vers la page d'où vient la requête ou vers la page du subraddot
        next_url = request.POST.get('next', f'/home/r/{name}/')
        return redirect(next_url)

    return redirect('social_app:subraddot_home', name=name)


@login_required
def leave_subraddot(request, name):
    if request.method == 'POST':
        subraddot = get_object_or_404(Subraddot, name=name)

        # Vérifier si l'utilisateur est le créateur (ne peut pas quitter son propre subraddot)
        if subraddot.creator == request.user:
            notify(request, "error", "Vous ne pouvez pas quitter un subraddot que vous avez créé!")
        elif request.user in subraddot.members.all():
            subraddot.members.remove(request.user)
            notify(request, "success", f"Vous avez quitté r/{subraddot.name}")
        else:
            notify(request, "info", f"Vous n'êtes pas membre de r/{subraddot.name}")

        # Redirection vers la page d'où vient la requête ou vers la page du subraddot
        next_url = request.POST.get('next', f'/home/r/{name}/')
        return redirect(next_url)

    return redirect('social_app:subraddot_home', name=name)
