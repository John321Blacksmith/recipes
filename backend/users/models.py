from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
	"""
	This custom user model
	extends a traditional one
	and brings more functionality.
	"""
	nickname = models.CharField(max_length=40)
