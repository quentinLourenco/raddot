from django.shortcuts import render
from social_app.models.Subraddot import Subraddot

def homepage(request):
    has_communities = False
    user_subscribed_communities = []
    user_created_communities = []

    # Vérifier si l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupérer les communautés créées par l'utilisateur
        user_created_communities = Subraddot.objects.filter(creator=request.user)

        # Note: comme le modèle d'abonnement n'est pas encore implémenté,
        # nous ne pouvons pas récupérer les communautés auxquelles l'utilisateur est abonné.
        # Cette partie sera à compléter ultérieurement
        # user_subscribed_communities = ...

        # Vérifier si l'utilisateur a des communautés
        has_communities = user_created_communities.exists()  # ou user_subscribed_communities.exists()

    context = {
        'title': 'Bienvenue sur Raddot',
        'has_communities': has_communities,
        'user_created_communities': user_created_communities,
        'user_subscribed_communities': user_subscribed_communities,
    }
    return render(request, 'social_app/homepage.html', context)
