"""
URL configuration for Atlas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:

"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('exercises/', views.exercises, name='exercises'),
    path('profile/', views.profile, name='profile'),
    path('foodie/', views.foodie, name='foodie'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('delete-exercise/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('delete-meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
]
