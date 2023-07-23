from rest_framework import serializers
from .tasks import send_feedback_message_task

 
class FeedBack:
	"""
	Feedback message blueprint.
	"""
	def __init__(self, email, subject, text):
		self.email = email
		self.subject = subject
		self.text = text


class FeedbackSerializer(serializers.Serializer):
	"""
	The feedback form the user
	sends to the servie.
	"""
	email = serializers.EmailField()
	subject = serializers.CharField()
	text = serializers.CharField()

	def create(self, validated_data):
		send_feedback_message_task.delay(
				validated_data['email'],
				validated_data['subject'],
				validated_data['text'],
			)
		return FeedBack(**validated_data)