from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.MainPageAPIView.as_view()),
    path('<str:category>/', views.CategoryRecipesAPIView.as_view()),
    path('recipes/<int:pk>/', views.RecipeDetailAPIView.as_view()),
    path('recipes/<int:pk>/new_comment', views.CommentCreationAPIView.as_view()),
]