from django.urls import path

from social_app.views.homepage import homepage
from social_app.views.my_subraddots import my_subraddots
from social_app.views.subraddot import create_subraddot, discover_subraddots, update_subraddot

urlpatterns = [
    path('', homepage, name='homepage'),

    path('r/discover/', discover_subraddots, name='discover_subraddots'),
    path('r/create/', create_subraddot, name='create_subraddot'),
    path('r/<str:name>/', homepage, name='subraddot_detail'),
    path('my_subraddots/', my_subraddots, name='my_subraddots'),

path('r/<str:name>/update/', update_subraddot, name='update_subraddot'),

]
