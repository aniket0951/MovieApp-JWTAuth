from .models import UsersInfo, WhiteListedToken, UserAddress
from rest_framework import serializers
from Utils.serializers import DynamicFieldsModelSerializer

class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersInfo
        fields = '__all__'
       


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
    
    def to_representation(self, instance):
        response_object = super().to_representation(instance)

        if instance.user:
            response_object["user"] = UsersInfoSerializer(instance.user).data

        return response_object       

class WhiteListedTokenSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WhiteListedToken
        fields = '__all__'