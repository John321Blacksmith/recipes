from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
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
    
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
class CategoryRecipesAPIView(ListModelMixin, GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'category'
    
    def get_object(self, request, category):
        try:
            category = Category.objects.get(title=category)
            return category
        except Category.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, category):
        category = self.get_object(request, category)
        if category:
            recipes = category.recipe_set.all()
            serializer = self.serializer_class(recipes, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status.HTTP_404_NOT_FOUND)

        
class RecipeDetailAPIView(RetrieveModelMixin, GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'recipe_id'
    
    def get_object(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            return recipe
        except Recipe.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def retrieve(self, request, recipe_id):
        recipe = self.get_object(request, recipe_id)
        if recipe:
            serializer = self.serializer_class(recipe)
            return Response(serializer.data)
        return Response(status.HTTP_404_NOT_FOUND)
        