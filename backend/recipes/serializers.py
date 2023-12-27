from rest_framework import serializers
from .models import Category, Ingredient, Recipe, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title']
        

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
    ingredients = serializers.SerializerMethodField('get_ingredients')
    category = serializers.SerializerMethodField('get_category_title')
    
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
            'ingredients',
            'directions',
            'comments'
        ]
        
    def get_category_title(self, obj):
        return obj.category.title
    
    def get_ingredients(self, obj):
        return [
            dict(ingredient) for ingredient in\
                IngredientSerializer(obj.ingredients.all(), many=True).data
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
    ingredients = IngredientSerializer(many=True)
    class Meta:
        model = Recipe
        fields = [
            'author',
            'title',
            'description',
            'prep_time',
            'cook_time',
            'directions',
            'ingredients'
        ]
    
    def create(self, validated_data):
        """
        Customize creation of the
        recipe object because 
        this method is normally
        not suported for nested
        fields like `ingredients`.
        """
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe_ingredients = [Ingredient.objects.get_or_create(**ingredient)[0].pk for ingredient in ingredients]
        recipe.ingredients.add(*recipe_ingredients)
        return recipe