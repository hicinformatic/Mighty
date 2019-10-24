from rest_framework.permissions import BasePermission

class HasMightyPermission(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        model = view.model()
        action = str(view.__class__.__name__)
        return request.user.has_perm(model.perm(action))