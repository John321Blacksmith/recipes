from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Recipe, Comment
from .serializers import RecipeSerializer, CommentSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def recipe_list(request, format=None):
	"""
	This view performs extraction
	of all the recipes from the DB.
	"""

	if request.method == 'GET':
		recipes = Recipe.objects.all()
		serializer = RecipeSerializer(recipes, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = RecipeSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail(request, pk, format=None):
	"""
	This view uses a parsed index
	of each pecipe and facilitates
	an object api endpoint.
	"""
	try:
		recipe = Recipe.objects.get(pk=pk)
	except Recipe.DoesNotExist:
		return Response(status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = RecipeSerializer(recipe)
		return Response(serializer.data)

	elif request.method == 'PUT':
		if request.user == recipe.author or request.user.is_staff:
			serializer = RecipeSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status.HTTP_201_CREATED)
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status.HTTP_403_FORBIDDEN)
		

	elif request.method == 'DELETE':
		if request.user == recipe.author:
			recipe.delete()
			return Response(status.HTTP_204_NO_CONTENT)
		else:
			return Response(status.HTTP_403_FORBIDDEN)

		
@api_view(['GET', 'POST'])
def recipe_comments(request, pk, format=None):
	"""
	This view parses the request to
	a collection api endpoint and uses
	a parsed index of recipe to extr
	act all the related comments.
	"""

	try:
		recipe = Recipe.objects.get(pk=pk)
	except Recipe.DoesNotExist:
		return Response(status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		comments = recipe.comment_set.all()
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)