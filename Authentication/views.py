from django.http import HttpResponse
from django.shortcuts import render
from yaml import serialize
from Utils.custome_viewsets import ModelViewSet
from .models import *
from .serializer import UsersInfoSerializer, UserAddressSerializer
from rest_framework.decorators import action
from Utils.exceptions import InvalidParameterException, UserNotFoundException, ValueMistMatchException, OTPExpiredException
from rest_framework.response import Response
from rest_framework import status
from Utils.utils import get_4_digit_otp, Messages
from datetime import timedelta, datetime
from rest_framework.serializers import ValidationError
from django.conf import settings
from Utils.custom_jwt_whitelisted_tokens import WhiteListedJWTTokenUtil
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from Utils.custome_permissions import IsPatientUser, IsMerchentUser, BlacklistUpdateMethodPermission
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from Utils.utils import *
from django.db.models import Count
from django.db.models import Q
from Merchent.models import TheterInformation
from Merchent.serilizer import TheterInformationSerializer


# Create your views here.
class UsersInfoModelViewSetAPIView(ModelViewSet):
    model = UsersInfo
    queryset =  UsersInfo.objects.all()
    serializer_class = UsersInfoSerializer
   
    
    create_success_message = 'Your registration completed successfully!'
    list_success_message = 'Users list returned successfully!'
    retrieve_success_message = 'User Information returned successfully!'
    update_success_message = 'User Information updated successfully!'

    data = {
        "data": None,
        "message": None,
    }

    def get_permissions(self):
        if self.action in ['list', 'create', ]:
            permission_classes = [IsPatientUser,]
            return [permission() for permission in permission_classes]
        
        if self.action in ['generate_verification_code', 'verify_generated_otp',]:
            permission_classes = [AllowAny]
            return [permission() for permission in permission_classes]

        if self.action in ['partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsPatientUser]
            return [permission() for permission in permission_classes]

        if self.action == 'update':
            permission_classes = [IsPatientUser | BlacklistUpdateMethodPermission]
            return [permission() for permission in permission_classes]

        return super().get_permissions()

    @action(detail=False, methods=['POST'])
    def generate_verification_code(self, request):
        
        mobile = self.request.data.get('mobile')

        if not mobile:
            raise InvalidParameterException
        
        user = self.get_queryset().filter(mobile=mobile).first()
        
        otp = get_4_digit_otp()
        otp_expiration_time = datetime.now(
         ) + timedelta(seconds=int(300))

        if user:
            user.otp = otp
            user.otp_expiration_time = otp_expiration_time
            user.save()
        else:
            user =  self.get_queryset().create(mobile=mobile,
                                               otp=otp, otp_expiration_time=otp_expiration_time)

            user.save()    

        data = {
            "mobile": mobile,
            "otp": otp
        }  

        self.data.update({
            "data":data,
            "message": "Otp generated successfully!"
        })

        return Response(self.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def verify_generated_otp(self, request):
        mobile = self.request.data.get('mobile')
        otp = self.request.data.get('otp')
        user_type = self.request.data.get('user_type')

        if not mobile or not otp:
            raise InvalidParameterException

        user = self.get_queryset().filter(mobile=mobile).first()

        if not user:
            raise UserNotFoundException

        if not user.otp == otp:
            raise ValueMistMatchException
        
        if datetime.now().timestamp() > user.otp_expiration_time.timestamp():
            raise OTPExpiredException
        message = "Login successful!"
        
        user.is_active = True
        if user_type:
            user.user_type = user_type
        user.save()

        serializer = self.get_serializer(user)
        payload = jwt_payload_handler(user)
        payload['username'] = str(serializer.data['id'])
        payload['mobile'] = mobile
        token = jwt_encode_handler(payload)
        expiration = datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
        expiration_epoch = expiration.timestamp()

        WhiteListedJWTTokenUtil.create_token(user, token)

        data = {
            "data": serializer.data,
            "message": message,
            "token": token,
            "token_expiration": expiration_epoch
        }
        return Response(data, status=status.HTTP_200_OK)

        
class UserAddressModelViewSetAPIView(ModelViewSet):
    model = UserAddress
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    create_success_message = "User Address created successfully"
    retrieve_success_message = "User Address retrieved successfully"
    list_success_message = "User Address list successfully"
    update_success_message = "User Address updated successfully"

    data = {
        "message":None,
        "data":None
    }

    def get_permissions(self):
        if self.action in ['list', 'create', 'get_therter_list_user_location' ]:
            permission_classes = [IsPatientUser,]
            return [permission() for permission in permission_classes]
        
        if self.action in ['partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsPatientUser]
            return [permission() for permission in permission_classes]
        return super().get_permissions()
    
    @action(detail=False, methods=['GET'])
    def TestFunctionObj(self, request):
        data = UserAddress.objects.all()
        for i in data:
            print(i.country)
        print(data)
        return HttpResponse("Data",  data)

    @action(detail=False, methods=['GET'])
    def get_therter_list_user_location(self, request):
        user_id = request.user.id       
        user_address = self.get_queryset().filter(Q(user__id=user_id)).first()

                # batch_limit = UserReferalcode.objects.aggregate(Count('batch_limit')).\
                #         filter(user=data.user).all()
        # data = self.get_queryset().aggregate(Count('state'))
        data = self.get_queryset().\
                          filter(Q(user__id=user_id)).\
                            annotate(Count('user__mobile')).\
                                count()
        # data = self.get_queryset().filter(Q(user__id=user_id)).values_list('state', flat=True)
        print("data count is", data)        

        if not user_address:
            raise ValidationError("User address not found")
   
        theter_info = TheterInformation.objects.filter(state=user_address.state, city=user_address.city).all()
        serializer = TheterInformationSerializer(theter_info, many=True)

        self.data.update({
            "data":serializer.data,
            "message":"Theter information returned successfully"
        })

        return Response(self.data, status=status.HTTP_200_OK)  
    
    @action(detail=False, methods=['GET'])
    def get_movies_by_theter_id(self, request):
        pass