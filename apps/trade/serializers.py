import time
from random import randint

from rest_framework import serializers
from alipay import AliPay

from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from Fresh_Ecommerce.settings import app_private_key_path, alipay_public_key_path, ali_app_id, return_url, notify_url

class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        'required': '请选择商品数量',
                                        'min_value': '商品数量至少为1'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.filter(is_delete=False))

    def create(self, validated_data):
        '''新增数据'''
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(is_delete=False, user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += 1
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改购物车商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    is_delete = serializers.BooleanField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        # 获取支付宝支付链接
        alipay = AliPay(
            appid=ali_app_id,
            app_notify_url=notify_url,
            app_private_key_string=open(app_private_key_path).read(),
            alipay_public_key_string=open(alipay_public_key_path).read(),
            sign_type="RSA2",
            debug=True,
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            subject='订单号：%s' % obj.order_sn,
            return_url=return_url,
            notify_url=notify_url
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        return pay_url

    def generate_order_sn(self):
        # 生成订单编号
        return '%s%d%d' % (time.strftime('%Y%m%d%H%M%S'), self.context['request'].user.id, randint(1000, 9999))

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        # 获取支付宝支付链接
        alipay = AliPay(
            appid=ali_app_id,
            app_notify_url=notify_url,
            app_private_key_string=open(app_private_key_path).read(),
            alipay_public_key_string=open(alipay_public_key_path).read(),
            sign_type="RSA2",
            debug=True,
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            subject='订单号：%s' % obj.order_sn,
            return_url=return_url,
            notify_url=notify_url
        )
        pay_url = alipay._gateway + '?' + order_string
        return pay_url

    class Meta:
        model = OrderInfo
        fields = '__all__'