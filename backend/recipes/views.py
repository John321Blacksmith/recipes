from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from .models import Recipe, Comment
from .serializers import RecipeSerializer, CommentSerializer
# Create your views here.


# The views below facilitate
# both collection & object API endpoints
# of recipes.
class RecipeList(generics.ListCreateAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer


# class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Recipe.objects.all()
# 	serializer_class = RecipeSerializer


# The view below facilitates
# collection API endpoints
# of comments.
# class CommentList(generics.ListCreateAPIView):
# 	serializer_class = CommentSerializer

# 	def get_queryset(self):
# 		"""
# 		Get only related comments.
# 		"""

@csrf_exempt
def recipe_detail(request, pk):
	"""
	This view uses a parsed index
	of each pecipe and facilitates
	an object api endpoint.
	"""
	try:
		recipe = Recipe.objects.get(pk=pk)
	except Recipe.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = RecipeSerializer(recipe)
		return JsonResponse(serializer.data, status=200)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = RecipeSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)

	elif request.method == 'DELETE':
		recipe.delete()
		return HttpResponse(status=204)

		
@csrf_exempt
def recipe_comments(request, pk):
	"""
	This view parses the request to
	a collection api endpoint and uses
	a parsed index of recipe to extr
	act all the related comments.
	"""

	try:
		recipe = Recipe.objects.get(pk=pk)
	except Recipe.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		comments = recipe.comment_set.all()
		serializer = CommentSerializer(comments, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CommentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)

	elif request.method == 'DELETE':
		recipe.delete()
		return HttpResponse(status=204)
