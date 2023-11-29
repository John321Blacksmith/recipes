from django.test import TestCase
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model
from .models import Recipe, Comment, Category
# Create your tests here.

class TestResipeLifeSpan(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            username='test',
            email='test@mail.com',
            password='test123'
        )
        cls.reviewer = get_user_model().objects.create_user(
            username='reviewer',
            email='reviewer@mail.com',
            password='reviewpassword'      
        )
        cls.category = Category.objects.create(title='Test category')
        cls.recipe = Recipe.objects.create(category=cls.category, 
                                           author=cls.user,
                                           title='Test',
                                           description='Testtesttest',
                                           date_published=datetime(2023, 11, 29, 13, 30, 55, 278206),
                                           prep_time=10.0,
                                           cook_time=30.0,
                                           directions='testhatprogram'
                                        )
        cls.comment = Comment.objects.create(
			recipe=cls.recipe,
			author=cls.reviewer,
			content='great test',
			date_published=datetime.now()
		)
        

























