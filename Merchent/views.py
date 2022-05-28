from django.shortcuts import render
from .models import TheterInformation, Screens
from .serilizer import TheterInformationSerializer, ScreensSerializer
from Utils.custome_viewsets import ModelViewSet

# Create your views here.
class TheterInformationModelViewSetAPIView(ModelViewSet):
    model = TheterInformation
    queryset = TheterInformation.objects.all()
    serializer_class = TheterInformationSerializer

    create_success_message = "Theter information has been created successfully"
    retrieve_success_message = "Theter information has been retrieved successfully"
    update_success_message = "Theter information has been updated successfully"
    list_success_message = "Theter information has been returned successfully"

    data = {
        "data": None,
        "message": None
    }

class ScreenModelViewSetAPIView(ModelViewSet):
    model = Screens
    queryset = Screens.objects.all()
    serializer_class = ScreensSerializer

    create_success_message = "Screen information has been created successfully"
    retrieve_success_message = "Screen information has been retrieved successfully"
    update_success_message = "Screen information has been updated successfully"
    list_success_message = "Screen information has been returned successfully"

    