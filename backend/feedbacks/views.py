from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FeedbackSerializer
# Create your views here.


class SendFeedbackAPI(APIView):
	"""
	Feedback API endpoint
	allows the user send
	his own opinion about
	the serice.
	"""
	def get_email(self, request):
		try:
			email = request.user.email
		except Exception:
			return None

		return email

	def get(self, request):
		"""
		enter the feedback page.
		"""
		email = self.get_email(request)
		serializer = FeedbackSerializer()
		return Response(serializer.data)

	def post(self, request):
		"""
		Send feedback.
		"""
		serializer = FeedbackSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
