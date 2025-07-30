from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from social_app.models.Subraddot import Subraddot
from social_app.models.Post import Post


@login_required
def create_post(request, name):
    """
    Vue pour créer un nouveau post dans un subraddot.
    """
    subraddot = get_object_or_404(Subraddot, name=name)

    # Vérifier si l'utilisateur est membre du subraddot
    if request.user != subraddot.creator and request.user not in subraddot.members.all():
        messages.error(request, "Vous devez être membre de cette communauté pour y publier.")
        return redirect('social_app:subraddot_home', name=name)

    if request.method == 'POST':
        title = request.POST.get('title')
        post_type = request.POST.get('post_type')

        if not title:
            messages.error(request, "Le titre est obligatoire.")
            return redirect('social_app:subraddot_home', name=name)

        # Créer un nouveau post
        post = Post(
            title=title,
            subraddot=subraddot,
            user=request.user,
            post_type=post_type
        )

        # Gérer le contenu selon le type de post
        if post_type == 'text':
            content = request.POST.get('content')
            post.content = content
        elif post_type == 'image':
            if 'image' in request.FILES:
                post.img = request.FILES['image']
            else:
                messages.error(request, "Veuillez sélectionner une image.")
                return redirect('social_app:subraddot_home', name=name)

        post.save()
        messages.success(request, "Votre post a été publié avec succès!")
        return redirect('social_app:subraddot_home', name=name)

    # Si la méthode n'est pas POST, rediriger vers la page du subraddot
    return redirect('social_app:subraddot_home', name=name)
