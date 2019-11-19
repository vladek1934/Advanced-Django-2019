from rest_framework.permissions import IsAuthenticated, BasePermission


class IsOwner(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_creator
