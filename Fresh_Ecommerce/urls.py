"""Fresh_Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

import xadmin
from .settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet

# Create a router and register our viewsets with it.

router = DefaultRouter()

# 配置goods的路由
router.register(r'goods', GoodsListViewSet, basename='goods')

# 配置categories的路由
router.register(r'categorys', CategoryViewSet, basename='categorys')

urlpatterns = [
       url(r'^xadmin/', xadmin.site.urls),
       url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

       # 商品列表页
       url(r'^', include(router.urls)),

       # 文档路由
       url(r'docs/', include_docs_urls(title='生鲜电商'))
]