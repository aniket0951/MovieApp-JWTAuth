from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from httplib2 import Response
from .models import TheterInformation, Screens, Seats
from .serilizer import TheterInformationSerializer, ScreensSerializer, SeatsSerializers
from Utils.custome_viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from Utils.exceptions import InvalidParameterException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from Utils.custome_permissions import IsPatientUser, IsMerchentUser, BlacklistUpdateMethodPermission

# Create your views here.
class TheterInformationModelViewSetAPIView(ModelViewSet):
    permission_classes = [IsAdminUser]
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

    def get_permissions(self):
        if self.action in ['list', 'create', ]:
            permission_classes = [IsAuthenticated,]
            return [permission() for permission in permission_classes]

        if self.action in ['partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsMerchentUser]
            return [permission() for permission in permission_classes]

        if self.action == 'update':
            permission_classes = [IsMerchentUser | BlacklistUpdateMethodPermission]
            return [permission() for permission in permission_classes]

        return super().get_permissions()

    @action(detail=False, methods=['GET'])
    def get_verify_theters(self, request):
        tag = self.request.data.get('requestfor')
        
        if tag == "verify":
            theters = self.get_queryset().filter(is_verify=True).all()

            if not theters:
                raise ValidationError("Currently no verify theter!")

            serializer = self.get_serializer(theters, many=True)
            self.data.update({
                "message":"Verify theter list return successfully",
                "data": serializer.data
            })
        elif tag == "unverify":
            theters = self.get_queryset().filter(is_verify=False).all()

            if not theters:
                raise ValidationError("Currently no un-verify theters!")

            serializer = self.get_serializer(theters, many=True)

            self.data.update({
                "message": "Unverify theter list return successfully!",
                "data": serializer.data
            })  
        else:
            raise InvalidParameterException     

        return Response(self.data, status=status.HTTP_200_OK)
     
class ScreenModelViewSetAPIView(ModelViewSet):
    model = Screens
    queryset = Screens.objects.all()
    serializer_class = ScreensSerializer

    create_success_message = "Screen information has been created successfully"
    retrieve_success_message = "Screen information has been retrieved successfully"
    update_success_message = "Screen information has been updated successfully"
    list_success_message = "Screen information has been returned successfully"

class SeatsModelViewSetAPIView(ModelViewSet):
    model = Seats
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializers

    create_success_message = "Seat information has been created successfully"
    retrieve_success_message = "Seat information has been retrieved successfully"
    update_success_message = "Seat information has been updated successfully"
    list_success_message = "Seat information has been returned successfully"