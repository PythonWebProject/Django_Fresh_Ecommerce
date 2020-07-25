import django_filters

from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''商品过滤类'''
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    min_price = django_filters.NumberFilter(field_name="market_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="market_price", lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['name', 'min_price', 'max_price']