from main.models import Image, Category
from main.Tools.analytics import userImageLabelAnalytics, imageLabelAnalytics, fullAnalytics, userAnalytics
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from main.serializers import UserImageAnalyticsSerializer, ImageAnalyticsSerializer, FullAnalyticsSerializer, \
    UserAnalyticsSerializer, FullAnalyticsSerializer2


class FullAnalytics2(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = FullAnalyticsSerializer2

# Useless functions for now


# class UserImageAnalytics(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserImageAnalyticsSerializer
#
#     def get_queryset(self):
#         try:
#             image = Image.objects.get(id=self.kwargs['imageId'])
#             user = self.request.user
#             stats = userImageLabelAnalytics(image, user)
#         except Image.DoesNotExist:
#             raise Http404
#         queryset = stats
#         return queryset
#
#
# class UserAnalytics(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserAnalyticsSerializer
#
#     def get_queryset(self):
#         try:
#             user = self.request.user
#             stats = userAnalytics(user)
#         except Image.DoesNotExist:
#             raise Http404
#         queryset = stats
#         return queryset
#
#
# class ImageAnalytics(generics.ListAPIView):
#     permission_classes = (IsAuthenticated, IsAdminUser)
#     serializer_class = ImageAnalyticsSerializer
#
#     def get_queryset(self):
#         try:
#             image = Image.objects.get(id=self.kwargs['imageId'])
#             stats = imageLabelAnalytics(image)
#         except Image.DoesNotExist:
#             raise Http404
#         queryset = stats
#         return queryset
#
#
# class FullAnalytics(generics.ListAPIView):
#     permission_classes = (IsAuthenticated, IsAdminUser)
#     serializer_class = FullAnalyticsSerializer
#
#     def get_queryset(self):
#         try:
#             stats = fullAnalytics(categoryId=self.kwargs['categoryId'])
#         except:
#             raise Http404
#         queryset = stats
#         return queryset
