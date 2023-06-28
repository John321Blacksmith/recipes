from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsUserOrReadOnly(BasePermission):
	"""
	This custom permission restricts
	both logged in or guests so they 
	only can check the user's info,
	but not alter.
	"""

	def has_object_permission(self, request, view, obj):

		# if the visiter is a guest or unrelated user,
		# the object remains 'read-only'
		if request.method in SAFE_METHODS:
			return True

		# if user is on his own details,
		# the object can be altered
		return request.user == obj.username