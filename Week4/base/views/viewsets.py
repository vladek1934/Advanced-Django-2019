from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import *

from base.serializers import *
from base.models import *


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = ()

    def get_queryset(self):
        print(self.request.user)
        return Profile.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return ProjectSerializer
    #     if self.action == 'create':
    #         return ProjectSerializer

    # def get_permissions(self):
    #     if self.action == 'destroy':
    #         return [IsAuthenticatedOwner()]
    #     return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        if self.action == 'destroy':
            return Project.objects.filter(creator=self.request.user)
        if self.action == 'update':
            return Project.objects.filter(creator=self.request.user)
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.request.user)
        return ProjectMember.objects.all()


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.request.user)
        return Block.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.request.user)
        return Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.creator:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.request.user == instance.creator:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.request.user)
        return TaskDocument.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.request.user)
        return TaskComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.creator:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.request.user == instance.creator:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
