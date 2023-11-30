from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.MainPageAPIView.as_view()),
    path('<str:category>/', views.CategoryRecipesAPIView.as_view()),
    path('<int:recipe_id>/', views.RecipeDetailAPIView.as_view()),
]