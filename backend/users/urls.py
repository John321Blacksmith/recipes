from django.urls import path
from . import views as user_view
from recipes import views as recipe_view


app_name = 'users'
urlpatterns = [
        path('profile/', user_view.UserProfileAPIView.as_view()),
        path('profile/new_recipe/', recipe_view.RecipeCreationAPIView.as_view()),
    ]
