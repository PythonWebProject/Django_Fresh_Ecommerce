from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage


class TerCategorySerializer(serializers.ModelSerializer):
    '''三级商品子类别序列化'''

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class SecCategorySerializer(serializers.ModelSerializer):
    '''二级商品子类别序列化'''

    sub_cat = TerCategorySerializer(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    '''一级商品类别序列化'''

    sub_cat = SecCategorySerializer(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ['image',]


class GoodsSerializer(serializers.ModelSerializer):
    '''商品序列化'''
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'