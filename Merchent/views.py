from django.shortcuts import render
from .models import TheterInformation
from .serilizer import TheterInformationSerializer
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
