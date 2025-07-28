from django.urls import path
from social_app.views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
]
