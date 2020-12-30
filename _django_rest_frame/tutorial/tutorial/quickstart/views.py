from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


# Create your views here.

# 使用视图集： 更好的组织视图逻辑
class UserViewSet(viewsets.ModelViewSet):
    """
    API接口：允许查看、编辑用户信息
    """
    # __doc__: 接口说明文档
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API接口：允许查看、编辑分组信息
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
