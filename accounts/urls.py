from django.urls import path

from .views import signup,userActivate ,dashboard



urlpatterns = [
    path('signup',signup),
    path('dashboard',dashboard),
    path('<str:username>/activate',userActivate)
]
