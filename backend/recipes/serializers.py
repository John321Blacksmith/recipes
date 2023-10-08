from rest_framework import serializers
from .models import Recipe, Comment


class RecipeSerializer(serializers.ModelSerializer):
	"""
	This class transforms
	all the recipe models to
	JSON API.
	"""

	# assign a comment collection variable for nested
	# response field
	comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all(), required=False) 

	class Meta:
		model = Recipe
		fields = ('id', 'title', 'date', 'ingredients', 'category', 'instruction', 'author', 'comments')


class CommentSerializer(serializers.ModelSerializer):
	"""
	This class transforms
	all the comments to JSON
	API.
	"""

	class Meta:
		model = Comment
		fields = ('id', 'author', 'date', 'content', 'recipe')