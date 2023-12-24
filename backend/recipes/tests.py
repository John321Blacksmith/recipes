from django.test import TestCase
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model
from .models import Recipe, Comment, Category, Ingredient
from .serializers import RecipeCreationSerializer
# Create your tests here.

class TestRecipeLifeSpan(TestCase):
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

        cls.meat = Category.objects.create(title='meat')
        cls.side_dish = Category.objects.create(title='side dish')

        cls.meat_recipe = Recipe.objects.create(
            author=cls.user,
            title='Delicious meat with sauce',
            description='This simple but tasty dish is favoured by millions because the meat is got very soft however the flash is red',
            directions='place a chunck of beef to the cold water and wait for one hour',
            prep_time=30,
            cook_time=50
        )


        cls.side_dish_recipe = Recipe.objects.create(
            author=cls.reviewer,
            title='Super flash potato',
            description='This dish is very simple but it can be accomaniment to any additions, including meat or fish',
            directions='first of all, prepare a pot of water, salt and then, put it on the stove',
            prep_time=40,
            cook_time=60
        )

        cls.unknown_recipe = Recipe.objects.create(
            author=cls.user,
            title='no title',
            description='no description',
            directions='no directions',
            prep_time=40,
            cook_time=60
        )

        cls.unknown_recipe1 = Recipe.objects.create(
            author=cls.user,
            title='no title1',
            description='no description1',
            directions='no directions1',
            prep_time=40,
            cook_time=60
        )
    
    def test_recipe_has_right_category(self):
        self.assertEqual(self.meat_recipe.category.title, 'meat')
        self.assertEqual(self.side_dish_recipe.category.title, 'side dish')
        self.assertEqual(self.unknown_recipe.category.title, 'diverse')


class TestRecipeCreationSerializer(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            username='test',
            email='test@mail.com',
            password='test123'
        )

        cls.meat = Category.objects.create(title='meat')        
        cls.side_dish = Category.objects.create(title='side dish')

        cls.side_dish_recipe_data = {
            "title": "Super flash potato",
            "description": "This dish is very simple but it can be accomaniment to any additions, including meat or fish",
            "directions": "first of all, prepare a pot of water, salt and then, put it on the stove",
            "prep_time": 47,
            "cook_time": 45
        }
        cls.serializer = RecipeCreationSerializer(data=cls.side_dish_recipe_data)