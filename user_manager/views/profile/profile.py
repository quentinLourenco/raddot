from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from social_app.components import TrophiesComponent


@login_required
def profile(request):
    user = request.user
    trophies = user.trophies.all()

    trophies_component = TrophiesComponent(trophies)
    context = trophies_component.get_context()

    return render(request, 'user_manager/profile.html', {
        'user': request.user,
        'trophies_context': context,
    })
