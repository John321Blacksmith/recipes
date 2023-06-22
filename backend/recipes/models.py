from django.db import models

# Create your models here.


class Recipe(models.Model):
	"""
	This model describes every
	recipe object with its base
	properties.
	"""
	title = models.CharField(max_length=100)
	ingredients = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=40)
	instruction = models.TextField()
	author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)



class Comment(models.Model):
	"""
	This model describes every
	comment object left from the
	user.
	"""
	author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) 
	content = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
