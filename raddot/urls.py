from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('social_app:homepage')
    else:
        return redirect('user_manager:login')

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('home/', include(('social_app.urls', 'social_app'), namespace='social_app')),
    path('auth/', include(('user_manager.urls', 'user_manager'), namespace='user_manager')),
    path('admin/', admin.site.urls),
]
