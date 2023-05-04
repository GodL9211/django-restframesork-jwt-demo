#! -*-conding=: UTF-8 -*-
# 2023/3/30 17:52


from rest_framework import serializers
from common.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'email', 'is_active', 'created_at',  'nickname']


if __name__ == '__main__':
    pass
