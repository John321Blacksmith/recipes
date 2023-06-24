from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	"""
	This custom form allows the customized
	user to be saved with one extra field.
	"""
	class Meta:
		model = CustomUser
		fields = UserCreationForm.Meta.fields + ('nickname',)


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = CustomUserCreationForm.Meta.fields
