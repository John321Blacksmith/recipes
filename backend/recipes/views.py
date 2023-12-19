from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Recipe
from .serializers import RecipeListSerializer, RecipeDetailSerializer, CommentSerializer, RecipeCreationSerializer


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

 
class RecipeDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    This view shows up a single recipe
    details and a list of related comments.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer]


class CommentCreationAPIView(GenericAPIView):
    """
    This view deals with the Comment
    creation process only and is invoked
    via a separate url.
    """
    queryset = Recipe.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        """
        This method works with a new comment
        object assembled through the frontend
        form.
        """
        return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class RecipeCreationAPIView(GenericAPIView):
    """
    Ths view provides a Recipe creation form
    and processes the form data.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        request.data['category'] = self.get_category(request.data).pk
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def get_category(self, request_data: dict):
        """
        Scrape the literal data
        a new object has and
        define a category it
        can be best related to.
        :return: category_pk <int>
        """
        # title, directions, description are literal fields
        
        # getting the literal data
        literal_data = ' '.join(val for val in [request_data[key] for key in ['title', 'directions', 'description']])
        
        # storage for words occurrencies
        word_frequency: dict[str, int] = {}
        
        # count the words and record results in the dict
        for word in literal_data.split(' '):
            if word in [key for key in word_frequency.keys()]:
                word_frequency[word] = word_frequency[word] + 1
            else:
                word_frequency[word] = 1
            
        # pick the occurred words from the storage
        # and check for existance of the categories
        # with such a title
        category_set = [
            # list of categories whose titles are in the 'most_occured' words list
            obj for obj in Category.objects.all() if obj.title.lower() in\
                # list of the most occurred words, not spaces
                [w.lower() for w, _ in word_frequency.items() if (_ > 0) and (w != ' ')]
            ]

        # if the recipe was not recognized, an undefined category object is retrived 
        return category_set[0].pk if len(category_set) == 1 else Category.objects.get_or_create(id=0, title='undefined')[0]
    