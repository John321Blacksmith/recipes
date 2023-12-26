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
        
        cls.pork = Ingredient.objects.get_or_create(title='pork')[0]
        cls.beef = Ingredient.objects.get_or_create(title='beef')[0]
        cls.salt = Ingredient.objects.get_or_create(title='salt')[0]
        cls.water = Ingredient.objects.get_or_create(title='water')[0]
        
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
    
    def test_meat_recipe_created(self):
        self.meat_recipe.ingredients.add(self.pork, self.salt)
        self.assertEqual(self.meat_recipe.ingredients.get(title='pork').title, 'pork')
        self.assertEqual(self.meat_recipe.ingredients.get(title='salt').title, 'salt')
    
    def test_another_recipe_created_with_common_ingrs_but_not_duplicated(self):
        new_ingr = Ingredient.objects.get_or_create(title='water')[0]
        self.side_dish_recipe.ingredients.add(self.salt, new_ingr)
        ingrs = [ing.title for ing in self.side_dish_recipe.ingredients.all()]
        self.assertIn('water', ingrs)
        self.assertIn('salt', ingrs)
        self.assertEqual(len(Ingredient.objects.all()), 4) # check if the list hasn't been changed
        
        
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

        cls.pork = Ingredient.objects.get_or_create(title='pork')[0]
        cls.beef = Ingredient.objects.get_or_create(title='beef')[0]
        cls.salt = Ingredient.objects.get_or_create(title='salt')[0]
        cls.water = Ingredient.objects.get_or_create(title='water')[0]
        
        cls.side_dish_recipe_data = {
            "author": 1,
            "title": "Super flash potato",
            "description": "This dish is very simple but it can be accomaniment to any additions, including meat or fish",
            "directions": "first of all, prepare a pot of water, salt and then, put it on the stove",
            "prep_time": 47,
            "cook_time": 45,
            "ingredients": [
                {"title": "potato"},
                {"title": "salt"}
            ]
        }
        cls.meat_recipe_data = {
            "author": 2,
            "title": "Vallish Pork with garlic flan",
            "description": "This dish is one of the tastest pork dishes in Wales",
            "directions": "Here is how to cook this fat dish. Place the meat stake and cut all the fat so no ladder is burnt in the oven.",
            "prep_time": 33,
            "cook_time": 23,
            "ingredients": [
                {"title": "salt"},
                {"title": "pork"}
            ]
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

        self.assertEqual(self.side_dish_recipe.category.title, 'side dish')
        self.assertEqual(self.meat_recipe.category.title, 'meat')
    
    def test_recipes_then_have_right_ingredients(self):
        self.side_dish_serializer.save()
        self.meat_serializer.save()
        
        self.side_dish_recipe = Recipe.objects.get(title=self.side_dish_recipe_data['title'])
        self.meat_recipe = Recipe.objects.get(title=self.meat_recipe_data['title'])
        
        s_d_ingrs = [ingr.title for ingr in self.side_dish_recipe.ingredients.all()]
        meat_ingrs = [ingr.title for ingr in self.meat_recipe.ingredients.all()]
        
        self.assertIn('potato', s_d_ingrs)
        self.assertIn('salt', s_d_ingrs)
        
        self.assertIn('salt', meat_ingrs)
        self.assertIn('pork', meat_ingrs)
        
    def test_ingredients_are_taken_from_the_request_with_titles(self):
        serializer = RecipeCreationSerializer(data=self.side_dish_recipe_data)
        self.assertIs(serializer.is_valid(), True)
        self.assertIsNotNone(serializer.save())
        recipe = Recipe.objects.get(title=self.side_dish_recipe_data['title'])
        self.assertIn('potato', [ing.title for ing in recipe.ingredients.all()])
        potato = Ingredient.objects.get(title='potato')
        self.assertIsNotNone(potato)
        self.assertEqual(potato.recipes.get(pk=1).pk, recipe.pk)