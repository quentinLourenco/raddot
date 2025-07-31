from django.shortcuts import render
from social_app.models.Subraddot import Subraddot
from django.db.models import Q

def discover_subraddots(request):
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('q', '').strip()

    if filter_type == 'created' and request.user.is_authenticated:
        subraddots = Subraddot.objects.filter(creator=request.user)
    elif filter_type == 'joined' and request.user.is_authenticated:
        subraddots = request.user.joined_subraddots.all()
    else:
        subraddots = Subraddot.objects.all()

    if search_query:
        subraddots = subraddots.filter(name__icontains=search_query)

    subraddots = subraddots.order_by('-created_at')

    context = {
        'subraddots': subraddots,
        'filter': filter_type,
        'title': 'Découvrir des subraddots'
    }

    return render(request, 'social_app/discover_subraddots.html', context)
