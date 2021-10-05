from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCreator(BasePermission):
    """Определение доступа к объявлению"""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.creator_id == request.user.id
