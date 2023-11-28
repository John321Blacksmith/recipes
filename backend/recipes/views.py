from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Recipe, Comment
from .serializers import CategorySerializer, RecipeSerializer, CommentSerializer


class MainPageAPIView(GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend]
    

class CategoryRecipesAPIView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer]


class RecipeDetailAPIView(GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    renderer_classes = [JSONRenderer]