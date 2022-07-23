from tabnanny import verbose
from django.db import models
import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class MyBaseModel(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    Custom model manager

    Arguments:
        BaseUserManager -- To define a custom manager that extends BaseUserManager
                                providing two additional methods

    Raises:
        TypeError -- It raises if the password is not provided while creating the users.

    Returns:
        user_object -- This will override the default model manager and returns user object.
    """

    def create_user(self, mobile=None, password=None):
        if mobile is None:
            raise TypeError('Users must have mobile number.')

        user = self.model(mobile=mobile, password=password)
        user.set_password(password)
        user.is_active = True     
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(mobile=mobile, password=password)
        user.is_active = True     
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin, MyBaseModel):
    """
    Class to create Custom Auth User Model

    Arguments:
        AbstractBaseUser -- Here we are subclassing the Django AbstractBaseUser,
                                which comes with only three fields:
                                1 - password
                                2 - last_login
                                3 - is_active
                            It provides the core implementation of a user model,
                                including hashed passwords and tokenized password resets.

        PermissionsMixin -- The PermissionsMixin is a model that helps you implement
                                permission settings as-is or
                                modified to your requirements.
    """

    mobile = PhoneNumberField(blank=True,
                              null=True,
                              unique=True,
                              verbose_name="Mobile Number")

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'mobile'
    objects = UserManager()
    username = 'mobile'

    class Meta:
        verbose_name = "Base User"
        verbose_name_plural = "Base Users"

    def __str__(self):
        return str(self.mobile)        

class UsersInfo(BaseUser):
    first_name = models.CharField(max_length=255, 
                            blank=True, 
                            null=True) 
    
    last_name = models.CharField(max_length=255,
                                 blank=True, 
                                 null=True) 

    otp = models.CharField(max_length=6,
                                 null=True,
                                 blank=True)                            

    otp_expiration_time = models.DateTimeField(
                                        blank=True,
                                        null=True,
                                        verbose_name='OTP Key Expiration DateTime')     

    user_type = models.CharField(max_length=25,
                                 default="AppUser",
                                 blank=False,
                                 null=False)                                                            
    
    # def __str__(self):
    #     return self.first_name

    def get_user_name(self):
        return self.first_name 
    
    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"

class UserAddress(MyBaseModel):
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

    user = models.ForeignKey(UsersInfo, on_delete=models.CASCADE,
                            related_name="user") 

    @property
    def class_status(self):
        if self.user.user_type == "Merchent":
            return str("You are a merchant")
        else:
            return str(self.user.id)                                               
    
    def __str__(self) -> str:
        return self.city
class WhiteListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(BaseUser, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")