from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.serializers import ProfileSerializer, UserSerializer
from base.models import Profile


class RegisterProfileAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = ()

    def get_queryset(self):
        print(self.request.user)
        return Profile.objects.all()
