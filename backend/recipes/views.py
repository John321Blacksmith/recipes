from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RecipeSerializer, CommentSerializer
from .models import Recipe, Comment
# Create your views here.
 

class RecipeList(APIView):
	"""
	This API collection endpoint
	enables GET and POST methods
	to get a list of the recipes
	and to create a new one.
	"""

	def get(self, request, format=None):
		recipes = Recipe.objects.all()
		serializer = RecipeSerializer(recipes, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		"""
		Create a new recipe if being
		logged in.
		"""
		request.data['author'] = request.user.id # specify a currently logged in user
		serializer = RecipeSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
	"""
	This API instance endpoint
	caries read, update and delete
	functionality.
	"""
	def get_object(self, pk):
		"""
		Retrieve an object
		from the DB via its
		ID.
		"""
		try:
			recipe = Recipe.objects.get(pk=pk)
		except Recipe.DoesNotExist:
			raise Http404
		return recipe

	def get(self, request, pk, format=None):
		"""
		Enable the API-consumer to 
		see details with each GET
		request to this endpoint.
		"""
		recipe = self.get_object(pk)
		serializer = RecipeSerializer(recipe)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		"""
		Enable the consumer to 
		change the recipe object
		which is his.
		"""
		recipe = self.get_object(pk)
		if request.user == recipe.author:
			serializer = RecipeSerializer(recipe, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status.HTTP_201_CREATED)
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status.HTTP_403_FORBIDDEN)

	def delete(self, request, pk, format=None):
		"""
		Enable the consumer to 
		delete his related recipes.
		"""
		recipe = self.get_object(pk)
		if request.user == recipe.author:
			recipe.delete()
			return Response(status.HTTP_204_NO_CONTENT)
		else:
			return Response(status.HTTP_403_FORBIDDEN)


class RecipeComments(APIView):
	"""
	This API endpoint has got
	both read and create
	functionality towards
	a list of comments related
	to a particular recipe object.
	"""
	
	def get_object(self, pk):
		"""
		"""
		try:
			recipe = Recipe.objects.get(pk=pk)
		except Recipe.DoesNotExist:
			raise Http404
		return recipe

	def get(self, request, pk, format=None):
		"""
		Enable the consumer
		to see a list of re
		lated comments.
		"""
		recipe = self.get_object(pk)
		# since the related name in the Comment model field is 'comments',
		# to access a set of recipe comments use the 'comments' attribute.
		comments = recipe.comments.all()  # fetch a list of comments
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request, pk, format=None):
		"""
		Enable the consumer to
		create a new comment
		instance against others.
		"""
		request.data['author'] = request.user.id
		request.data['recipe'] = pk
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

