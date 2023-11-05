from django.db import models
 
# Create your models here.

class Category(models.Model):
	"""
	This model represents a whole
	group of the recipes.
	"""
	title = models.CharField(max_length=255)

	def __str__(self):
		return self.title


class Recipe(models.Model):
	"""
	This model describes every
	recipe object with its base
	properties.
	"""
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=1000, verbose_name='description')
	date_published = models.DateTimeField(auto_now_add=True)
	prep_time = models.IntegerField(verbose_name='preperation time')
	cook_time = models.IntegerField(verbose_name='cook time')
	directions = models.TextField(verbose_name='directions')
	author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	

class Ingredients(models.Model):
	"""
	This model represents a 
	dedicated table of
	ingredients. 
	"""
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Ingredient(models.Model):
	"""
	This model represents a
	single ingredient.
	"""
	ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	volume = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='amount or volume')

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
	date_published = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(choices=[(1, 'very bad'), (2, 'bad'), (3, 'passable'), (4, 'good'), (5, 'excellent')])

	def __str__(self):
		return self.content[:40]