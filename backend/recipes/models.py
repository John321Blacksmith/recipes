from django.db import models
from .dataset import categories

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
	
	def get_category(self, dataset: dict[str, set]) -> str:
		"""
		Receive a list of literal
		data and category dataset
		and categorize the recipe
		"""
		# get common words stats
		word_ratio = {k: len({val for val in self.literal_data} & v) for k, v in dataset.items()}
		
		# convert the word-common ratio
		# pairs to tuples
		tups = [(w, r) for w, r in word_ratio.items() if r > 0]

		# find the greatest ratio
		if len(tups) > 0:
			most_possible = tups[0]
			for i in range(len(tups)):
				if tups[i][1] > most_possible[1]:
					most_possible = tups[i]

			return most_possible[0]
		return None

	@property
	def literal_data(self) -> list[str]:
		"""
		Take all the literal
		data from the recipe
		object and gather it
		in one data structure
		"""
		all_words = []
		for l_field in [l for l in self.__dict__.values() if isinstance(l, str)]:
			for w in l_field.split():
				all_words.append(w.lower())
		return all_words
	
	def save(self, *args, **kwargs):
		"""
		Associate a recipe object
		to the existing category
		or mark as 'diverse'.
		Then save the recipe.
		"""
		try:
			self.category = Category.objects.get(title=self.get_category(categories))
		except Category.DoesNotExist:
			self.category = Category.objects.get_or_create(title='diverse')[0]

		super().save(*args, **kwargs)


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