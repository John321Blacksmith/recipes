from rest_framework import generics
from .models import Recipe, Comment
from .serializers import RecipeSerializer, CommentSerializer
# Create your views here.


# The views below facilitate
# both collection & object API endpoints
# of recipes.
class RecipeList(generics.ListAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer


# The view below facilitates
# collection API endpoints
# of comments.
class CommentList(generics.ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer