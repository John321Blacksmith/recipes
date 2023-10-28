from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'recipes'

urlpatterns = [
	path('recipes/', views.RecipeList.as_view()),
	path('recipes/<int:pk>/', views.RecipeDetail.as_view()),
	path('recipes/<int:pk>/comments/', views.RecipeComments.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)