from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class CustomUserTest(TestCase):
	"""
	This test checks if the user
	is created and saved correctly.
	"""

	@classmethod
	def setUpTestData(cls):
		cls.user = get_user_model().objects.create_user(
					username='Test User',
					nickname='User123',
					email='user123@mail.com',
					password='test123',
			)

	def test_user_registered(self):
		"""
		Check if the user is signed up.
		"""
		self.assertEqual(get_user_model().objects.all().count(), 1)
		self.assertEqual(get_user_model().objects.all()[0].username, 'Test User')
		self.assertEqual(get_user_model().objects.all()[0].nickname, 'User123')
		self.assertEqual(get_user_model().objects.all()[0].email, 'user123@mail.com')
		
# the test passed