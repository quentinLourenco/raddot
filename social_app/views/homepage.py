from django.shortcuts import render
from social_app.models.Subraddot import Subraddot


def homepage(request):
    has_subraddots = False
    user_subscribed_subraddots = []
    user_created_subraddots = []

    # Vérifier si l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupérer les communautés créées par l'utilisateur
        user_created_subraddots = Subraddot.objects.filter(creator=request.user)

        # Note: comme le modèle d'abonnement n'est pas encore implémenté,
        # nous ne pouvons pas récupérer les communautés auxquelles l'utilisateur est abonné.
        # Cette partie sera à compléter ultérieurement
        # user_subscribed_subraddots = ...

        # Vérifier si l'utilisateur a des communautés
        has_subraddots = user_created_subraddots.exists()  # ou user_subscribed_subraddots.exists()

    context = {
        'title': 'Bienvenue sur Raddot',
        'has_csubraddots': has_subraddots,
        'user_created_subraddots': user_created_subraddots,
        'user_subscribed_subraddots': user_subscribed_subraddots,
    }
    return render(request, 'social_app/homepage.html', context)
