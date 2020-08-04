from django.db.models import Q
from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


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


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = SecCategorySerializer(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_instance = ad_goods[0].goods
            goods_json = GoodsSerializer(good_instance, many=False, context={'request': self.context['request']}).data
        return goods_json

    class Meta:
        model = GoodsCategory
        fields = '__all__'