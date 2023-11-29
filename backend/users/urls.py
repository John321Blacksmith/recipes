from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
	path('', views.CustomUserList.as_view()),
	path('<int:pk>/', views.CustomUserDetail.as_view()),
	path('<int:pk>/recipes/', views.UserRecipesList.as_view()),
	path('<int:pk>/comments/', views.UserCommentsList.as_view()),
]