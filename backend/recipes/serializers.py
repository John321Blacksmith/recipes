from rest_framework import serializers
from .models import Category, Recipe, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    comments_amount = serializers.SerializerMethodField('get_comments_amount')
    author = serializers.SerializerMethodField('get_author_name')
    category = serializers.SerializerMethodField('get_cetegory_title')
    class Meta:
        model = Recipe
        fields = [
            'pk',
            'category',
            'author',
            'title',
            'date_published',
            'comments_amount'
        ]
    
    def get_comments_amount(self, obj):
        return len(obj.comments.all())
    
    def get_author_name(self, obj):
        return obj.author.username
    
    def get_cetegory_title(self, obj):
        return obj.category.title
    

class RecipeDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_comments')
    class Meta:
        model = Recipe
        fields = [
            'pk',
            'category',
            'author',
            'title',
            'description',
            'date_published',
            'prep_time',
            'cook_time',
            'directions',
            'comments'
        ]

    def get_comments(self, obj):
        return [
            dict(comment) for comment in\
                CommentSerializer(obj.comments.all(), many=True).data
        ]
        

class RecipeCreationSerializer(serializers.ModelSerializer):
    """
    This serializer processes the the fields
    of the Recipe object used at recipe creation.
    """
    class Meta:
        model = Recipe
        fields = [
            'author',
            'category',
            'title',
            'description',
            'prep_time',
            'cook_time',
            'directions'
        ]
        
        def get_category(self, obj):
            """
            Scrape the literal data
            a new object has and
            define a category it
            can be best related to.
            :return: category_pk <int>
            """
            # title, directions, description are literal fields
            # getting the literal data
            
            literal_data = ' '.join(val for val in [obj.__dict__[key] for key in ['title', 'directions', 'description']])
            # storage for words occurrencies
            word_frequency = {}
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
                    [   # list of the most occurred words, not spaces
                        w.lower() for w, _ in word_frequency.items() if (_ > 0) and (w != ' ')
                        ]
                ]
            
            return category_set[0].pk