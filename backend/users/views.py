from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import CustomUserSerializer
from .models import CustomUser
# Create your views here.


class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    """
    This view shows up a profile
    info with the related content
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes  = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)