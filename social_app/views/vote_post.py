from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse

from social_app.models import VotePost, Post


@login_required
@require_http_methods(["POST"])
def vote_post(request):
    """
    Vue pour gérer les votes sur les posts via formulaire classique
    """
    post_id = request.POST.get('post_id')
    vote_value = request.POST.get('value')

    if not post_id:
        messages.error(request, 'Post non trouvé')
        return redirect('home')  # Remplacez par votre URL de redirection

    try:
        post = get_object_or_404(Post, id=post_id)
        vote_value = int(vote_value) if vote_value else 0

        # Récupérer le vote existant s'il existe
        try:
            existing_vote = VotePost.objects.get(user=request.user, post=post)

            if vote_value == 0:
                # Supprimer le vote
                existing_vote.delete()
            else:
                # Modifier le vote existant
                existing_vote.value = vote_value
                existing_vote.save()

        except VotePost.DoesNotExist:
            # Créer un nouveau vote (seulement si value n'est pas 0)
            if vote_value != 0:
                VotePost.objects.create(
                    user=request.user,
                    post=post,
                    value=vote_value
                )

    except (ValueError, TypeError):
        messages.error(request, 'Valeur de vote invalide')
    except Exception as e:
        messages.error(request, 'Une erreur est survenue lors du vote')

    # Rediriger vers la page précédente ou la page du post
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    else:
        # Fallback - rediriger vers la page du post si elle existe
        try:
            return redirect('post_detail', pk=post.id)  # Ajustez selon votre URL
        except:
            return redirect('home')  # Fallback final