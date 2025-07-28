from django.shortcuts import render

def homepage(request):
    context = {
        'title': 'Bienvenue sur Raddot',
        'user': request.user,
    }
    return render(request, 'social_app/homepage.html', context)
