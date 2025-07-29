from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'user_manager/profile.html', {
        'user': request.user
    })
