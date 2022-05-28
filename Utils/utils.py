from django.utils.crypto import get_random_string
from Authentication.models import UsersInfo
from Utils.exceptions import InvalidParameterException, UserNotFoundException

def get_4_digit_otp():
    OTP_LENGTH = 4
    generation_code = get_random_string(
            length=OTP_LENGTH, allowed_chars='0123456789')

    return generation_code       

def get_6_digit_otp():
    OTP_LENGTH = 6
    generation_code = get_random_string(
        length=OTP_LENGTH, allowed_chars='01234567898'
    )        

    return generation_code

class Messages():
    
    def otp_generation_success():
        msg = "OTP generation successfully created"
        return msg

def get_enduser_object(request):
    try:
        user = UsersInfo.objects.get(mobile=request.user)
        return user 
    except Exception as e:     
        print("Exception: %s" % e)
    return None