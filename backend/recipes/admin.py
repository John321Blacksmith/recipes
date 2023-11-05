from django.contrib import admin
from .models import Recipe, Comment, Category, Ingredients, Ingredient
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Ingredients)
admin.site.register(Ingredient)


