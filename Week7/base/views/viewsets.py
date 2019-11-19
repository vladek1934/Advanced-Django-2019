import logging

from django.core.mail.backends import console
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import *

from base.serializers import *
from base.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.request.user)
        return Profile.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if self.action in ['destroy', 'create', 'update']:
            return Project.objects.filter(creator=self.request.user)
        else:
            return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        actions_logger.info(
            f"{self.request.user} created project {serializer.data.get('id'), serializer.data.get('name')}!\n")
        # serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        actions_logger.warning(f"{instance.creator} deleted project {instance.id, instance.name}!\n")
        instance.delete()

    @action(methods=['GET'], detail=False)
    def my_projects(self, request):
        projects = Project.objects.filter(creator=self.request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def my_membership(self, request):
        project_ids = self.request.user.projects
        print(project_ids)
        projects = Project.objects.all()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def blocks(self, request, pk):
        instance = self.get_object()
        serializer = BlockSerializer(instance.blocks, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def members(self, request, pk):
        instance = self.get_object()
        serializer = ProjectMemberSerializer(instance.members, many=True)
        return Response(serializer.data)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        projects = Project.objects.filter(creator=self.request.user)
        return ProjectMember.objects.filter(project__in=projects)

    def perform_create(self, serializer):
        serializer.save()
        actions_logger.info(
            f"{self.request.user} added user {serializer.data.get('user')} to project {serializer.data.get('project')}!\n")

    def perform_destroy(self, instance):
        actions_logger.warning(
            f"{self.request.user} removed user {instance.user} from project {instance.project.id, instance.project.name}!\n")
        instance.delete()


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.request.user)
        return Block.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update']:
            return TaskFullSerializer
        else:
            return TaskShortSerializer

    def get_queryset(self):
        if self.action in ['destroy', 'update']:
            return Task.objects.filter(creator=self.request.user)
        else:
            return Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_queryset(self):
        if self.action in ['destroy', 'update']:
            return TaskDocument.objects.filter(creator=self.request.user)
        else:
            return TaskDocument.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        actions_logger.info(
            f"{self.request.user} uploaded document {serializer.data.get('id'), serializer.data.get('document')}!\n")
        # serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        actions_logger.warning(f"{instance.creator} deleted document {instance.id, instance.document}!\n")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action in ['destroy', 'update']:
            return TaskComment.objects.filter(creator=self.request.user)
        else:
            return TaskComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
