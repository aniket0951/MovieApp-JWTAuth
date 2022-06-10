import re
from rest_framework import permissions
from Authentication.models import UsersInfo

DO_NOT_HAVE_PERMISSION = "You do not have permission to do this action."


class IsPatientUser(permissions.BasePermission):
    """
    Is Patient User
    """
    message = 'You do not have permission to access this information.'

    def has_permission(self, request, view):
        """
        Checking if the user is Patient.
        """
        try:
            if hasattr(request.user, 'mobile') and UsersInfo.objects.filter(mobile=request.user.mobile).exists():
                return True
        except Exception:
            pass
        self.message = 'Patient has the permission to perform this action.'
        return False

class IsMerchentUser(permissions.BasePermission):
    message = 'You do not have permission to access this information.'

    def has_object_permission(self, request, view, obj):
        try:
            if hasattr(request.user, 'mobile') and UsersInfo.objects.filter(mobile=request.user.mobile, user_type="AppUser").exists():
                return True
        except Exception:
            pass
        self.message = "Merchent has the permission to perform this action."
        return False       

def user_object(request):
    try:
        if request.user and request.user.id:
            return UsersInfo.objects.get(id=request.user.id)
    except Exception as error:
        print(str(error))
    return None        

class BlacklistUpdateMethodPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted UPDATE method.
    """
    message = DO_NOT_HAVE_PERMISSION

    def has_permission(self, request, view):
        return request.method != 'PUT'

    def has_object_permission(self, request, view, obj):
        return request.method != 'PUT'


class BlacklistPartialUpdateMethodPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted Partial UPDATE method.
    """
    message = DO_NOT_HAVE_PERMISSION

    def has_permission(self, request, view):
        return request.method != 'PATCH'

    def has_object_permission(self, request, view, obj):
        return request.method != 'PATCH'


class BlacklistDestroyMethodPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted UPDATE method.
    """
    message = DO_NOT_HAVE_PERMISSION

    def has_permission(self, request, view):
        return request.method != 'DELETE'

    def has_object_permission(self, request, view, obj):
        return request.method != 'DELETE'
