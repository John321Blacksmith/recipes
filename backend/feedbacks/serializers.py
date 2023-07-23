from time import sleep
from django.core.mail import send_mail
from rest_framework import serializers


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
		sleep(10)
		send_mail(
				subject=validated_data['subject'],
				message=f"{validated_data['text']}\n Thank you for your feedback!",
				from_email="super-recipes.com",
				recipient_list=[validated_data['email']],
				fail_silently=False,
			)
		return FeedBack(**validated_data)