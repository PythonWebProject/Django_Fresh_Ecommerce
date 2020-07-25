import json

from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers

from goods.models import Goods


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)


class GoodsListView(View):
    def get(self, request):
        '''通过serializers实现商品列表页'''
        goods = Goods.objects.all()[:10]
        json_data = serializers.serialize('json', goods)
        return JsonResponse(json.loads(json_data), safe=False)