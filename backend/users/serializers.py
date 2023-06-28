from rest_framework import serializers
from recipes.models import Comment
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
	"""
	This instance transforms a user's model
	to the JSON API.
	"""
	# related user's comments
	comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

	class Meta:
		model = CustomUser
		fields = ('id', 'username', 'nickname', 'email', 'comments')