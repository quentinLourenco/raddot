from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required

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

            messages.success(request, f"Le subraddot '{subraddot.name}' a été créé avec succès!")
            # return redirect('social_app:subraddot_detail', name=subraddot.name)
    else:
        form = CreateSubraddotForm()

    return render(request, 'social_app/subraddot_create.html', {
        'form': form,
        'title': 'Créer un subraddot',
    })


def subraddots_list(request):
    subraddots = Subraddot.objects.all()
    return render(request, 'social_app/subraddots_list.html', {
        'title': 'Découvrir des subraddots',
        'subraddots': subraddots,
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
            messages.success(request, f"La communauté r/{subraddot.name} a été mise à jour avec succès!")
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
        'is_creator': request.user == subraddot.creator if request.user.is_authenticated else False,
        'is_member': False,
    }

    return render(request, 'social_app/subraddot_home.html', context)


def user_subraddots(request):
    user_subraddots = Subraddot.objects.filter(creator=request.user).order_by('-created_at')

    return render(request, 'social_app/my_subraddots.html', {
        'subraddots': user_subraddots,
        'title': 'Mes subraddots',
    })
