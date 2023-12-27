from rest_framework import serializers
from recipes.models import Comment
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
	"""
	This instance transforms a user's model
	to the JSON API.
	"""
	comments_amount = serializers.SerializerMethodField('get_comments_ammount')
	recipes_amount = serializers.SerializerMethodField('get_recipes_amount')
	class Meta:
		model = CustomUser
		fields = [
			'id', 
			'username', 
			'nickname', 
			'email',
			'comments_amount', 
			'recipes_amount'
		]
	
	def get_comments_ammount(self, obj):
		return len(obj.comments.all())

	def get_recipes_amount(self, obj):
		return len(obj.recipe_set.all())