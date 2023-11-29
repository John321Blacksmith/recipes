from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.renderers import JSONRenderer, HTMLFormRenderer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Recipe, Comment
from .serializers import CategorySerializer, RecipeSerializer, CommentSerializer


class MainPageAPIView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    
    
class CategoryRecipesAPIView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer]


class RecipeDetailAPIView(GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    renderer_classes = [JSONRenderer]