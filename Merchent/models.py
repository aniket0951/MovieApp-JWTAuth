from django.db import models
import uuid
from Authentication.models import MyBaseModel, UsersInfo
from phonenumber_field.modelfields import PhoneNumberField


class TheterInformation(MyBaseModel):
    name = models.CharField(max_length=255, 
                            blank=False,
                            null=False)

    address = models.CharField(max_length=255, 
                               blank=False,
                               null=False) 

    contact = PhoneNumberField(blank=False,
                              null=False,
                              unique=True,
                              verbose_name="Theter Contact")  

    country = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            default="India")

    state = models.CharField(max_length=255,
                            blank=False,
                            null=False)

    city = models.CharField(max_length=255,
                            blank=False,
                            null=False)   

    user = models.ForeignKey(UsersInfo, on_delete=models.PROTECT, related_name="merchent_user",
                            null=True, blank=True)     

    is_active = models.BooleanField(default=False, 
                                    blank=True, null=True)    

    is_verify = models.BooleanField(default=False,
                                    blank=True, null=True)                                                                       

class Screens(MyBaseModel):

    screen_name = models.CharField(max_length=255,
                                   blank=False, 
                                   null=False) 

    screen_type = models.CharField(max_length=255,
                                   blank=True,  
                                   null=True, 
                                   default="Class-3")

    is_active = models.BooleanField(default=False,
                                    blank=True,
                                    null=True)

    theter = models.ForeignKey(TheterInformation, 
                               on_delete=models.CASCADE, 
                               related_name="theter")                                                                                           