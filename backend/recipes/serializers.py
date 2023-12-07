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