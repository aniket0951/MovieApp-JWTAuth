from rest_framework import serializers
from .models import TheterInformation
from Authentication.serializer import UsersInfoSerializer

class TheterInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheterInformation
        fields = '__all__'

    def to_representation(self, instance):
        response_object = super().to_representation(instance)

        if instance.user:
            response_object['user'] = UsersInfoSerializer(instance.user).data

        return response_object     