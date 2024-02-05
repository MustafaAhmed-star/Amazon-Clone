from django.urls import path

from .views import signup,userActivate



urlpatterns = [
    path('signup',signup),
    path('<str:username>/activate',userActivate)
]
