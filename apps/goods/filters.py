import django_filters
from django.db.models import Q

from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''商品过滤类'''
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    pricemin = django_filters.NumberFilter(field_name="market_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="market_price", lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        '''自定义过滤'''
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['name', 'pricemin', 'pricemax', 'is_hot']