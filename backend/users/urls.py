from django.urls import path
from recipes import views


app_name = 'users'
urlpatterns = [ 
        path('profile/new_recipe/', views.RecipeCreationAPIView.as_view()),
    ]
