from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, CommentSerializer
from .permissions import IsUserOrReadOnly


# Create your views here.

class CustomUserList(APIView):
	"""
	List all the authorized users.
	"""
	permission_classes = [IsUserOrReadOnly]
	def get(self, request, format=None):
		"""
		Inspect a list of users.
		"""
		users = CustomUser.objects.all()
		serializer = CustomUserSerializer(users, many=True)
		return Response(serializer.data)


class CustomUserDetail(APIView):
	"""
	Display the info and a bunch
	of recipes and reviews of a
	particular user.
	"""
	permission_classes = [IsUserOrReadOnly]
	def get_object(self, pk):
		try:
			user = CustomUser.objects.get(pk=pk)
		except CustomUser.DoesNotExist:
			raise Http404

		return user

	def get(self, request, pk, format=None):
		"""
		See the details of a user.
		"""
		serializer = CustomUserSerializer(self.get_object(pk))
		return Response(serializer.data)

	def put(self, request, pk):
		"""
		The only present user can change his
		profile.
		"""
		user = self.get_object(pk)
		serializer = CustomUserSerializer(user, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		"""
		The only owner of his account
		can delete it.
		"""
		user = self.get_object(pk)
		user.delete()
		return Response(status.HTTP_204_NO_CONTENT)


class UserRecipesList(APIView):
	"""
	List all the recipes a
	particular user has created.
	"""
	permission_classes = [IsUserOrReadOnly]
	def get_object(self, pk):
		try:
			user = CustomUser.objects.get(pk=pk)
		except CustomUser.DoesNotExist:
			raise Http404

		return user 

	def get(self, request, pk, format=None):
		"""
		Fetch the related recipes via
		users id.
		"""
		# pull out the recipes
		user = self.get_object(pk)
		recipes = user.recipe_set.all()
		serializer = RecipeSerializer(recipes, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		"""
		Only the present user can add
		recipes to his collection.
		"""
		user = self.get_object(pk)
		serializer = RecipeSerializer(data=request.data)


class UserCommentsList(APIView):
	"""
	List all comments the user has 
	submitted.
	"""
	def get_object(self, pk):
		try:
			user = CustomUser.objects.get(pk=pk)
		except CustomUser.DoesNotExist:
			raise Http404
		return user

	def get(self, request, pk):
		user = self.get_object(pk)
		comments = user.comments.all()
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)
