from django.urls import path
from . import views

urlpatterns = [
    path('cooking-suggestion/', views.cooking_suggestion, name='cooking_suggestion'),
    path('cooking_suggestion/', views.cooking_suggestion, name='cooking_suggestion'),
]