import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from Fresh_Ecommerce.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    '''短信发送序列化'''

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''验证手机号码'''


        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号格式有误，请重新输入')

        # 验证手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('手机号已经被注册过，请更换手机号重新注册或直接使用该手机号登录')

        # 验证短信发送频率
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('验证码发送频率过快，请稍后再试')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''用户序列化'''
    code = serializers.CharField(max_length=4, min_length=4, label='验证码', write_only=True,
                                 help_text='验证码',
                                 error_messages={
                                     'required': '请输入验证码',
                                     'blank': '请输入验证码',
                                     'max_length': '请输入4位验证码',
                                     'min_length': '请输入4位验证码'
                                 })
    username = serializers.CharField(required=True, allow_blank=False,  label='用户名', validators=[UniqueValidator(queryset=User.objects.filter(is_delete=False), message='用户已经存在')])
    password = serializers.CharField(label='密码',  write_only=True, style={'input_type': 'password'})

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        # 验证验证码是否存在
        if verify_records:
            last_record = verify_records[0]
            five_minute_ago = datetime.now() - timedelta(minutes=5)
            # 验证验证码是否过期
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError('验证码已过期，请重新验证')
            # 验证验证码是否正确
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('数据有误，请重新验证')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'code', 'mobile', 'password']