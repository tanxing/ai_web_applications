from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cooking-suggestion/", views.cooking_suggestion, name="cooking_suggestion"),
    path("cooking_suggestion/", views.cooking_suggestion, name="cooking_suggestion"),
    path("gemini-inference/", views.gemini_inference, name="gemini_inference"),
    path("gemini_inference/", views.gemini_inference, name="gemini_inference"),
]
