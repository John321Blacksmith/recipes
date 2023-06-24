from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = [
		'email',
		'username',
		'nickname',
		'is_staff',
	]
	fileldsets = UserAdmin.fieldsets + ((None, {'fields': ('nickname',)}),)
	add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('nickname',)}),)


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)