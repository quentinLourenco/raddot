from django.shortcuts import render
from social_app.models.Subraddot import Subraddot


def homepage(request):
    joined_subraddots = []
    posts = []
    if request.user.is_authenticated:
        user = request.user
        joined_subraddots = user.joined_subraddots.all().order_by('-created_at')
        for subraddot in joined_subraddots:
            last_post = subraddot.posts.all().order_by('-created_at')[:1]
            if last_post:
                posts.append(last_post[0])

    has_joined_subraddot = bool(joined_subraddots)
    context = {
        'title': 'Bienvenue sur Raddot',
        'has_joined_subraddot': has_joined_subraddot,
        'posts' : posts,
    }

    return render(request, 'social_app/homepage.html', context)

