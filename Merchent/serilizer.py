from pyexpat import model
from attr import field
from rest_framework import serializers
from .models import TheterInformation, Screens, Seats
from Authentication.serializer import UsersInfoSerializer
from Utils.serializers import DynamicFieldsModelSerializer

class TheterInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheterInformation
        fields = '__all__'

    def to_representation(self, instance):
        response_object = super().to_representation(instance)

        if instance.user:
            response_object['user'] = UsersInfoSerializer(instance.user).data

        return response_object   

class ScreensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screens
        fields = '__all__'

    def to_representation(self, instance):
        response_object = super().to_representation(instance)

        if instance.theter:
            response_object['theter'] = TheterInformationSerializer(instance.theter).data

        return response_object 

class SeatsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = '__all__'

    def to_representation(self, instance):
        response_object =  super().to_representation(instance) 

        if instance.screen:
            response_object['screen'] = ScreensSerializer(instance.screen).data

        return response_object       