from django.urls import path
from social_app.views.homepage import homepage
from social_app.views.subraddot import create_subraddot

urlpatterns = [
    path('', homepage, name='homepage'),
    path('r/create/', create_subraddot, name='create_subraddot'),
    path('r/<str:name>/', homepage, name='subraddot_detail'),  # Placeholder pour l'instant
]
