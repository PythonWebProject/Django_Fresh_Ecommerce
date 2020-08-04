from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.

class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        用户收藏列表
    create:
        创建用户收藏
    retrieve:
        用户收藏详情
    destroy:
        删除用户收藏
    '''
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserFavSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user, is_delete=False)

    def get_serializer_class(self):
        '''动态设置序列化'''
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer

    # def perform_create(self, serializer):
    #     '''重写实现收藏数'''
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()


class LeavingMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        留言列表
    create:
        添加留言
    delete:
        删除留言
    '''

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user, is_delete=False)


class AddressViewSet(viewsets.ModelViewSet):
    '''
    收货地址管理
    list:
        收货地址列表
    create:
        新建收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    '''

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user, is_delete=False)