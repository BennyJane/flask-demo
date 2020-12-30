# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : _django_rest_frame
# Time       ：2020/12/27 10:27
# Warning    ：The Hard Way Is Easier
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
