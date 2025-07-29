from django.urls import path

from social_app.views.homepage import homepage
from social_app.views.subraddot import subraddot_create, subraddot_update, subraddot_home, \
    user_subraddots, join_subraddot, leave_subraddot
from social_app.views.discover import discover_subraddots

urlpatterns = [
    path('', homepage, name='homepage'),
    path('r/create/', subraddot_create, name='subraddot_create'),
    path('r/<str:name>/', subraddot_home, name='subraddot_home'),
    path('my_subraddots/', user_subraddots, name='user_subraddots'),
    path('r/<str:name>/update/', subraddot_update, name='update_subraddot'),
    path('discover/', discover_subraddots, name='discover_subraddots'),
    path('r/<str:name>/join/', join_subraddot, name='join_subraddot'),
    path('r/<str:name>/leave/', leave_subraddot, name='leave_subraddot'),
]
