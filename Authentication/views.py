from django.shortcuts import render
from yaml import serialize
from Utils.custome_viewsets import ModelViewSet
from .models import *
from .serializer import UsersInfoSerializer
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
from Utils.custome_permissions import IsPatientUser, user_object, BlacklistUpdateMethodPermission
from rest_framework.permissions import AllowAny

# Create your views here.
class UsersInfoModelViewSetAPIView(ModelViewSet):
    permission_classes = [AllowAny]
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

        if self.action in ['partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsPatientUser]
            return [permission() for permission in permission_classes]

        if self.action == 'update':
            permission_classes = [BlacklistUpdateMethodPermission]
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


        

class VerifyUsersModelViewSetAPIView(ModelViewSet):
    permission_classes = [ IsPatientUser ]
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
            permission_classes = [AllowAny,]
            return [permission() for permission in permission_classes]

        if self.action in ['partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsPatientUser]
            return [permission() for permission in permission_classes]

        if self.action == 'update':
            permission_classes = [BlacklistUpdateMethodPermission]
            return [permission() for permission in permission_classes]

        return super().get_permissions()


    @action(detail=False, methods=['GET'])
    def get_verify_users(self, request):  
        user = user_object(request)
        data = self.get_serializer(user)
        return Response(data.data, status=status.HTTP_200_OK)  