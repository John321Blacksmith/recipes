from rest_framework import serializers
from .models import Recipe, Comment


class RecipeSerializer(serializers.ModelSerializer):
	"""
	This class transforms
	all the recipe models to
	JSON API.
	"""

	class Meta:
		model = Recipe
		fields = ('id', 'title', 'date', 'ingredients', 'category', 'instruction', 'author')


class CommentSerializer(serializers.ModelSerializer):
	"""
	This class transforms
	all the comments to JSON
	API.
	"""

	class Meta:
		model = Comment
		fields = ('id', 'author', 'date', 'content', 'recipe')