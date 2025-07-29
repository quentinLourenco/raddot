from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_app.models.Subraddot import Subraddot

@login_required
def my_subraddots(request):
    user_subraddots = Subraddot.objects.filter(creator=request.user).order_by('-created_at')

    return render(request, 'social_app/my_subraddots.html', {
        'subraddots': user_subraddots,
        'title': 'Mes communautés',
    })
