from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required

from social_app.forms.create_subraddot import CreateSubraddotForm
from social_app.models.Subraddot import Subraddot
from social_app.forms.update_subraddot import UpdateSubraddotForm
from social_app.models.Post import Post

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

def discover_subraddots(request):
    subraddots = Subraddot.objects.all()
    return render(request, 'social_app/discover_subraddots.html', {
        'title': 'Découvrir des subraddots',
        'subraddots': subraddots,
    })

def update_subraddot(request, name):
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

    return render(request, 'social_app/update_subraddot.html', {
        'form': form,
        'subraddot': subraddot
    })

def subraddot_detail(request, name):
    subraddot = get_object_or_404(Subraddot, name=name)

    posts = Post.objects.filter(subraddot=subraddot).order_by('-created_at')

    context = {
        'subraddot': subraddot,
        'posts': posts,
        'is_creator': request.user == subraddot.creator if request.user.is_authenticated else False,
        'is_member': False,
    }

    return render(request, 'social_app/subraddot_detail.html', context)
