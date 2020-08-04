from rest_framework import mixins, viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilter


# Create your views here.

class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    商品列表页，并实现分页、搜索、过滤、排序
    list:
        商品列表
    retrieve:
        商品详情
    '''

    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Goods.objects.filter(is_delete=False).order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = GoodsFilter
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'shop_price']

    def retrieve(self, request, *args, **kwargs):
        '''重写实现点击数'''
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表
    retrieve:
        商品分类详情
    '''

    queryset = GoodsCategory.objects.filter(category_type=1).filter(is_delete=False)
    serializer_class = CategorySerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        轮播图列表
    '''
    queryset = Banner.objects.filter(is_delete=False).order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类数据
    '''

    queryset = GoodsCategory.objects.filter(is_delete=False, is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer
