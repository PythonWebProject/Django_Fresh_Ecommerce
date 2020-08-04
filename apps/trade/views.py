from datetime import datetime

from alipay import AliPay
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from Fresh_Ecommerce.settings import app_private_key_path, alipay_public_key_path, ali_app_id

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    '''
    list:
        购物车列表
    create:
        加入购物车
    update:
        购物车修改
    delete:
        删除购物车
    '''

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = ShoppingCartSerializer
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user, is_delete=False)

    def perform_create(self, serializer):
        '''创建购物车更新库存量'''
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        '''删除购物车更新库存量'''
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        '''修改购物车更新库存量'''
        existed_record = ShoppingCart.objects.filter(is_delete=False).get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    订单管理
    list:
        订单列表
    delete:
        删除订单
    create:
        新增订单
    '''

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user, is_delete=False)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user, is_delete=False)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order


class AliPayView(APIView):
    '''
    get:
        处理支付宝return_url请求
    post:
        处理支付宝notify_url请求
    '''

    alipay = AliPay(
        appid=ali_app_id,
        app_notify_url=None,
        app_private_key_string=open(app_private_key_path).read(),
        alipay_public_key_string=open(alipay_public_key_path).read(),
        sign_type="RSA2",
        debug=True,
    )

    def get(self, request):

        data = dict(request.GET.items())
        signature = data.pop("sign", None)
        print(data)
        success = self.alipay.verify(data, signature)
        order_sn = data.get('out_trade_no', None)
        print(success)
        trade_status = self.alipay.api_alipay_trade_query(out_trade_no=order_sn).get("trade_status", None)
        print(trade_status)
        if success and trade_status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            trade_no = data.get('trade_no', None)
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn, is_delete=False)
            if existed_orders:
                for order in existed_orders:
                    order_goods = order.goods.all()
                    for order_good in order_goods:
                        goods = order_good.goods
                        goods.sold_num += order_good.goods_num
                        goods.save()
                    order.pay_status = trade_status
                    order.trade_no = trade_no
                    order.pay_time = datetime.now()
                    order.save()
                response = HttpResponseRedirect('http://127.0.0.1:8080/#/app/home/member/order')
                response.set_cookie('nextPath', 'pay', max_age=2)
                print('cookie', response.cookies)
                return response
        return HttpResponseRedirect('http://127.0.0.1:8080/#/app/shoppingcart/cart')

    def post(self, request):
        data = dict(request.POST.items())
        signature = data.pop("sign", None)
        success = self.alipay.verify(data, signature)
        order_sn = data.get('out_trade_no', None)
        trade_status = self.alipay.api_alipay_trade_query(out_trade_no=order_sn).get("trade_status", None)
        if success and trade_status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            trade_no = data.get('trade_no', None)
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn, is_delete=False)
            print(len(existed_orders))
            if existed_orders:
                for order in existed_orders:
                    order_goods = order.goods.all()
                    for order_good in order_goods:
                        goods = order_good.goods
                        goods.sold_num += order_good.goods_num
                        goods.save()
                    order.pay_status = trade_status
                    order.trade_no = trade_no
                    order.pay_time = datetime.now()
                    order.save()
                response = HttpResponseRedirect('http://127.0.0.1:8080/#/app/home/member/order')
                response.set_cookie('nextPath', 'pay', max_age=2)
                print('cookie', response.cookies)
                return response
        return HttpResponseRedirect('http://127.0.0.1:8080/#/app/shoppingcart/cart')