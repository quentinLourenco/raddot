from django.urls import path, include
from django.shortcuts import redirect
from user_manager.views.profile.profile import profile
from user_manager.views.profile.update_profile import update_profile
from django.conf import settings
from django.conf.urls.static import static

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('social_app:homepage')
    else:
        return redirect('user_manager:login')

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('home/', include(('social_app.urls', 'social_app'), namespace='social_app')),
    path('auth/', include(('user_manager.urls', 'user_manager'), namespace='user_manager')),
    path('profile/', profile, name='profile'),
    path('profile/edit/', update_profile, name='update_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
