from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import DONE

class IsAuthAndDone(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in ["get","post","put","delete"]:
            return True

        return request.user.status == DONE

class IsAuthDoneAndOwner(BasePermission):
    def has_permission(self, request, view):
       if not request.user.is_authenticated:
            return False
       if request.method in ["get","post","put","delete"]:
            return True
       return request.user.status == DONE

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

