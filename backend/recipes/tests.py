from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe, Comment

# Create your tests here.


class Recipe_and_Comment_model_data_test(TestCase):
	"""
	In this test the models Recipe and Comment
	are checked if anything works as expected.
	"""

	@classmethod
	def setUpTestData(cls):
		cls.recipe_author = get_user_model().objects.create_user(
					username='test user',
					email='test@mail.com',
					password='test123',
			)

		cls.another_user = get_user_model().objects.create(
					username='another user',
					email='test2@mail.com',
					password='test1234',
			)

		cls.recipe = Recipe.objects.create(
					title='test',
					ingredients='test, test',
					category='testing',
					instruction='test instruction',
					author=cls.recipe_author,
		)

		cls.comment = Comment.objects.create(
					author=cls.another_user,
					recipe=cls.recipe,
					content='that is a good test',
			)

	def test_recipe_model_data(self):
		"""
		Check if the recipe model data
		is saved correctly.
		"""
		self.assertEqual(self.recipe.title, 'test')
		self.assertEqual(self.recipe.ingredients, 'test, test')
		self.assertEqual(self.recipe.category, 'testing')
		self.assertEqual(self.recipe.instruction, 'test instruction')
		self.assertEqual(self.recipe.author.username, 'test user')

	def test_comment_model_data(self):
		"""
		Check if the comment model
		data is saved correctly.
		"""
		
		self.assertEqual(self.comment.author.username, 'another user')
		self.assertEqual(self.comment.recipe, self.recipe)
		self.assertEqual(self.comment.content, 'that is a good test')

# passed