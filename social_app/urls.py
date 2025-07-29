from django.urls import path

from social_app.views.homepage import homepage
from social_app.views.subraddot import subraddot_create, subraddots_list, subraddot_update, subraddot_home, \
    user_subraddots

urlpatterns = [
    path('', homepage, name='homepage'),

    path('r/discover/', subraddots_list, name='subraddots_list'),
    path('r/create/', subraddot_create, name='subraddot_create'),
    path('r/<str:name>/', subraddot_home, name='subraddot_home'),
    path('my_subraddots/', user_subraddots, name='user_subraddots'),
    path('r/<str:name>/update/', subraddot_update, name='update_subraddot'),

]
