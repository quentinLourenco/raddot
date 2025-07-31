from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from social_app.models.Subraddot import Subraddot
from social_app.models.Post import Post
from social_app.models.Trophy import Trophy  # Ajout de l'import
from social_app.forms.create_comment import CreateCommentForm
from social_app.utils.trophies import check_trophies, check_first_post, check_five_post


@login_required
def create_post(request, name):
    subraddot = get_object_or_404(Subraddot, name=name)

    if request.user != subraddot.creator and request.user not in subraddot.members.all():
        messages.error(request, "Vous devez être membre de cette communauté pour y publier.")
        return redirect('social_app:subraddot_home', name=name)

    if request.method == 'POST':
        title = request.POST.get('title')
        post_type = request.POST.get('post_type')

        if not title:
            messages.error(request, "Le titre est obligatoire.")
            return redirect('social_app:subraddot_home', name=name)

        post = Post(
            title=title,
            subraddot=subraddot,
            user=request.user,
            post_type=post_type
        )

        if post_type == 'text':
            content = request.POST.get('content')
            post.content = content
        elif post_type == 'image':
            if 'img' in request.FILES:
                post.img = request.FILES['img']
            else:
                messages.error(request, "Veuillez sélectionner une image.")
                return redirect('social_app:subraddot_home', name=name)

        post.save()
        check_first_post(request.user)
        check_five_post(request.user)
    return redirect('social_app:subraddot_home', name=name)

@require_POST
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CreateCommentForm(request.POST)
    referer = request.META.get('HTTP_REFERER', '/')
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        messages.success(request, "Votre commentaire a été ajouté avec succès!")
    else:
        messages.error(request, "Le contenu du commentaire ne peut pas être vide.")
    return redirect(referer)
