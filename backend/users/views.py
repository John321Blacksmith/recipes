from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView
from .serializers import CustomUserSerializer
from .models import CustomUser
# Create your views here.


class UserProfileAPIView(GenericAPIView):
    """
    This view shows up a profile
    info with the related content
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]