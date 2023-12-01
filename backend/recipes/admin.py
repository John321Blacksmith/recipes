from django.contrib import admin
from .models import Recipe, Comment, Category, Ingredient
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Ingredient)


