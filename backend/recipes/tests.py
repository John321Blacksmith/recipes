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
        cls.reviewer = get_user_model().objects.create_user(
            username='reviewer',
            email='reviewer@mail.com',
            password='reviewpassword'      
        )


        cls.meat = Category.objects.create(title='meat')        
        cls.side_dish = Category.objects.create(title='side dish')

        cls.side_dish_recipe_data = {
            "author": 1,
            "title": "Super flash potato",
            "description": "This dish is very simple but it can be accomaniment to any additions, including meat or fish",
            "directions": "first of all, prepare a pot of water, salt and then, put it on the stove",
            "prep_time": 47,
            "cook_time": 45
        }
        cls.meat_recipe_data = {
            "author": 2,
            "title": "Vallish Pork with garlic flan",
            "description": "This dish is one of the tastest pork dishes in Wales",
            "directions": "Here is how to cook this fat dish. Place the meat stake and cut all the fat so no ladder is burnt in the oven.",
            "prep_time": 33,
            "cook_time": 23
        }
        cls.side_dish_serializer = RecipeCreationSerializer(data=cls.side_dish_recipe_data)
        cls.meat_serializer = RecipeCreationSerializer(data=cls.meat_recipe_data)
        cls.side_dish_is_valid = cls.side_dish_serializer.is_valid()
        cls.meat_is_valid = cls.meat_serializer.is_valid()
    
    def test_both_serializers_are_valid(self):
        self.assertIs(self.side_dish_is_valid, True)
        self.assertIs(self.meat_is_valid, True)
    
    def test_serializers_save_data_correctly(self):
        self.side_dish_serializer.save()
        self.meat_serializer.save()

        self.side_dish_recipe = Recipe.objects.get(title=self.side_dish_recipe_data['title'])
        self.meat_recipe = Recipe.objects.get(title=self.meat_recipe_data['title'])
        
        self.assertEqual(self.side_dish_recipe.description, self.side_dish_recipe_data['description'])
        self.assertEqual(self.meat_recipe.description, self.meat_recipe_data['description'])
    