from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
       if request.method in permissions.SAFE_METHODS:
           return True
       else:
           return bool(request.user and request.user.is_staff)
       

class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map = {
            'GET':  ['%(app_label)s.view_%(model_name)s'],
            'POST': ['%(app_label)s.add_%(model_name)s'],
            'PUT': ['%(app_label)s.change_%(model_name)s'],
            'PATCH': ['%(app_label)s.change_%(model_name)s'],
            'DELETE': ['%(app_label)s.delete_%(model_name)s'],
        }


class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')