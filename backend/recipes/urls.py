from django.urls import path, include
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register('recepies', views.RecipeViewSet)
# router.register('comments', views.CommentViewSet)

app_name = 'recipes'

urlpatterns = [
	path('recipes/', views.RecipeList.as_view()),
	path('recipes/<int:pk>/', views.RecipeDetail.as_view()),
	path('recipes/<int:pk>/comments/', views.CommentList.as_view()),
] 