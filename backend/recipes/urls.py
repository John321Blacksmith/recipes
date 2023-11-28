from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('recipes/', views.MainPageAPIView.as_view()),
    path('recipes/<str:title>/', views.CategoryRecipesAPIView.as_view()),
    path('recipes/<int:recipe_id>/', views.RecipeDetailAPIView.as_view()),
]