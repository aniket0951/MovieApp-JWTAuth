from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidParameterException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid_request'
    default_detail = 'Please provide a required parameters!'

class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'not_found'
    default_detail = 'User not found!'

class ValueMistMatchException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'not_found'
    default_detail = 'Otp mismatch!'    

class OTPExpiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'otp_expired'
    default_detail = 'OTP is expired!'    