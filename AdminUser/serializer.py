from pyexpat import model

from attr import fields
from .models import Movies
from rest_framework.serializers import ModelSerializer

class MovieSerializers(ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'
        