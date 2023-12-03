from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Recipe, Comment
from .serializers import RecipeListSerializer, RecipeDetailSerializer, CommentSerializer


class MainPageAPIView(ListAPIView):
    """
    This view renders the recipes
    regardless a category.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']      
    
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
class CategoryRecipesAPIView(ListModelMixin, GenericAPIView):
    """
    This view lists the recipes
    belong to a particular category
    only.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
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

        
class RecipeDetailAPIView(GenericAPIView):
    """
    This view shows the details of a
    particular recipe with a comments
    section with a comment form inside.
    """
    queryset = Recipe.objects.all()
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            return recipe
        except Recipe.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        self.recipe = self.get_object(request, pk)
        if self.recipe:
            serializer = self.get_serializer(Recipe)(self.recipe)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status.HTTP_404_NOT_FOUND)
    
    def post(self, request, pk):
        serializer = self.get_serializer(Comment)(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        recipe = self.get_object(request, pk)
        if recipe:
            recipe.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk):
        recipe = self.get_object(request, pk)
        if recipe:
            serializer = self.get_serializer(Comment)(data=request.data)
            serializer.update()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_403_FORBIDDEN)
    
    def get_serializer(self, model):
        return type(
                f"{str(model)[str(model).index('.')+1:-2]}Serializer",
                (serializers.ModelSerializer,),
                {
                    'Meta':
                        type(
                            'Meta',
                            (object,),
                                {
                                    'model': model, 'fields': '__all__'
                                }
                        )
                }
            )