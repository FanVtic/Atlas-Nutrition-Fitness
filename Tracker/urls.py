from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exercises, name='exercises'),
    path('profile/', views.profile, name='profile'),
    path('foodie/', views.foodie, name='foodie'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
