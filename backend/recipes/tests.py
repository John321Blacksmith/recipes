from django.test import TestCase
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model
from .models import Recipe, Comment, Category, Ingredient
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
        cls.category = Category.objects.create(title='Test category')
        cls.category2 = Category.objects.create(title='Test category2')
        cls.recipe = Recipe.objects.create(category=cls.category, 
                                           author=cls.user,
                                           title='Test',
                                           description='Testtesttest',
                                           date_published=datetime(2023, 11, 29, 13, 30, 55, 278206),
                                           prep_time=10.0,
                                           cook_time=30.0,
                                           directions='testhatprogram'
                                        )
        cls.recipe2 = Recipe.objects.create(category=cls.category2, 
                                           author=cls.reviewer,
                                           title='Test2',
                                           description='Testtesttest2',
                                           date_published=datetime(2023, 12, 29, 13, 30, 55, 278206),
                                           prep_time=10.0,
                                           cook_time=30.0,
                                           directions='testhatprogram2'
                                        )
        cls.recipe2 = Recipe.objects.create(category=cls.category2, 
                                           author=cls.reviewer,
                                           title='Test2',
                                           description='Testtesttest2',
                                           date_published=datetime(2023, 12, 29, 13, 30, 55, 278206),
                                           prep_time=10.0,
                                           cook_time=30.0,
                                           directions='testhatprogram2'
                                        )
        
        cls.test_ing1, cls.test_ing2, cls.test_ing3 = Ingredient(title='Ingredient1'), Ingredient(title='Ingredient2'), Ingredient(title='Ingredient3')
        cls.not_unique_ing = Ingredient(title='Ingredient2')
        
        cls.comment1 = Comment.objects.create(
			recipe=cls.recipe,
			author=cls.reviewer,
			content='great test',
			date_published=datetime.now()
		)
        cls.comment2 = Comment.objects.create(
			recipe=cls.recipe,
			author=cls.reviewer,
			content='super test',
			date_published=datetime.now()
		)
        [ing.save() for ing in (cls.test_ing1, cls.test_ing2, cls.test_ing3, cls.not_unique_ing)]
        cls.recipe.ingredients.add(cls.test_ing1, cls.test_ing2, cls.test_ing3) # first recipe completed
        
        cls.ing_titles = [obj['title'] for obj in Ingredient.objects.values('title')]
    
    def database_doesnot_have_duplicate_ingredients(self):
        self.assertEqual(['Ingredient1', 'Ingredient2', 'Ingredient3'], self.ing_titles)
    
    def test_recipe_belongs_to_right_category(self):
        self.assertIs(self.recipe.category, self.category)
        self.assertEqual(self.recipe.category.title, 'test category')
    
    def test_recipe_belongs_to_right_author(self):
        self.assertIs(self.recipe.author, self.user)
        self.assertEqual(self.recipe.author.username, 'test')
        
    def test_comments_belongs_to_right_author(self):
        self.assertEqual(self.comment1.author, self.reviewer)
        self.assertEqual(self.comment1.author.username, self.reviewer.username)
        
        self.assertEqual(self.comment2.author, self.reviewer)
        self.assertEqual(self.comment2.author.username, self.reviewer.username)
        
    def test_comments_belongs_to_right_recipe(self):
        self.assertIs(self.comment1.recipe, self.recipe)
        self.assertEqual(self.comment1.recipe.title, 'Test')
        
        self.assertIs(self.comment2.recipe, self.recipe)
        self.assertEqual(self.comment2.recipe.title, 'Test')
    
    def test_recipe_has_right_data(self):
        self.assertEqual(self.recipe.title, 'Test')
        self.assertEqual(self.recipe.description, 'Testtesttest')
        # self.assertEqual(self.recipe.date_published, datetime(2023, 11, 29, 13, 30, 55, 278206))
        self.assertEqual(self.recipe.prep_time, 10.0)
        self.assertEqual(self.recipe.cook_time, 30.0)
        self.assertEqual(self.recipe.directions, 'testhatprogram')
        self.assertCountEqual(['Ingredient1', 'Ingredient2', 'Ingredient3'], self.ing_titles)
        self.assertEqual(len(self.recipe.comments.all()), 2)
    
    def test_category_data(self):
        self.assertEqual(self.recipe.category.title, 'test category')
    
    def test_the_ingredient_duplicate_not_created_but_existing_is_appended_to_recipe(self):
        ...
        
    def test_undefined_recipe_category(self):
        ...