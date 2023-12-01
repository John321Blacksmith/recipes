from django.db import models
 
# Create your models here.

class Category(models.Model):
	"""
	This model represents a whole
	group of the recipes.
	"""
	title = models.CharField(max_length=255)

	class Meta:
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.title.capitalize()

	def save(self, *args, **kwargs):
		self.title = self.title.lower()
		super().save(*args, **kwargs)


class Recipe(models.Model):
	"""
	This model describes every
	recipe object with its base
	properties.
	"""
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=1000, verbose_name='description')
	date_published = models.DateTimeField(auto_now_add=True)
	prep_time = models.IntegerField(verbose_name='preperation time')
	cook_time = models.IntegerField(verbose_name='cook time')
	directions = models.TextField(verbose_name='directions')

	def __str__(self):
		return self.title


class Ingredient(models.Model):
	"""
	This model represents a
	single ingredient.
	"""
	recipes = models.ManyToManyField(Recipe, related_name='ingredients')
	title = models.CharField(max_length=50)

	class Meta:
		verbose_name = 'ingredient'
		verbose_name_plural = 'ingredients'

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.title not in [obj['title'] for obj in Ingredient.objects.values('title')]:
			super().save(*args, **kwargs)
  
 
class Comment(models.Model):
	"""
	This model describes every
	comment object left from the
	user.
	"""
	recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
	author = models.ForeignKey('users.CustomUser', related_name='comments', on_delete=models.CASCADE)
	content = models.TextField()
	date_published = models.DateTimeField(auto_now_add=True)
	# the ratings are collected from each comment, and an overall rating is assigned to the recipe

	class Meta:
		verbose_name = 'comment'
		verbose_name_plural = 'comments'

	def __str__(self):
		return self.content[:40]