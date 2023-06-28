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

	def __str__(self):
		return self.title



class Comment(models.Model):
	"""
	This model describes every
	comment object left from the
	user.
	"""
	author = models.ForeignKey('users.CustomUser', related_name='comments', on_delete=models.CASCADE)
	recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE) 
	content = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content[:40]