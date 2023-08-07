# _*_coding:utf-8_*_

import logging

from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# from apps.finance.models import *
from xj_user.models import Platform

logger = logging.getLogger(__name__)


class UserPlatformSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='platform_name')
    platform = serializers.ReadOnlyField(source='platform_name')

    class Meta:
        model = Platform
        fields = [
            # 'platform_id',
            # 'platform_name',
            'value',
            'platform',
        ]


# 获取平台列表
# class UserPlatform(generics.UpdateAPIView):  # 或继承(APIView)
class UserPlatform(generics.UpdateAPIView):  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    serializer_class = UserPlatformSerializer
    params = None

    def get(self, request, *args, **kwargs):
        self.params = request.query_params  # 返回QueryDict类型

        platforms = Platform.objects.all()
        serializer = UserPlatformSerializer(platforms, many=True)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': serializer.data,
        })
