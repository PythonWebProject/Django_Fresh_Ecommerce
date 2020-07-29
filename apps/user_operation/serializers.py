from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        fields = ['id', 'user', 'goods']
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.filter(is_delete=False),
                fields=['user', 'goods'],
                message='请勿重复收藏'
            )
        ]