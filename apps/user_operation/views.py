from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.

class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''用户收藏'''
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserFavSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user, is_delete=False)