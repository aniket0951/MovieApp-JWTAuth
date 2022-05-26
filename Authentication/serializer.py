from .models import UsersInfo, WhiteListedToken
from rest_framework import serializers
from Utils.serializers import DynamicFieldsModelSerializer

class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersInfo
        fields = '__all__'

class WhiteListedTokenSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WhiteListedToken
        fields = '__all__'