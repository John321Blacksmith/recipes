from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.

class CustomUserList(APIView):
	"""
	List all the authorized users.
	"""
	
	def get(self, request):
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

	def get_object(self, pk):
		try:
			user = CustomUser.objects.get(pk=pk)
		except CustomUser.DoesNotExist:
			raise Http404

		return user

	def get(self, request, pk):
		"""
		See the details of a user.
		"""
		serializer = CustomUserSerializer(self.get_object(pk))
		return Response(serializer.data)
