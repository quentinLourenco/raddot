from django.shortcuts import render
from social_app.models.Subraddot import Subraddot

def discover_subraddots(request):
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'created' and request.user.is_authenticated:
        subraddots = Subraddot.objects.filter(creator=request.user).order_by('-created_at')
    elif filter_type == 'joined' and request.user.is_authenticated:
        subraddots = request.user.joined_subraddots.all().order_by('-created_at')
    else:
        subraddots = Subraddot.objects.all().order_by('-created_at')

    context = {
        'subraddots': subraddots,
        'filter': filter_type,
        'title': 'Découvrir des subraddots'
    }

    return render(request, 'social_app/discover_subraddots.html', context)
