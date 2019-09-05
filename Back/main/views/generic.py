from main.models import Image, Polygon, User, Category, Comment, Label, Folder
from main.serializers import ImageSerializer, PolygonSerializer, CategorySerializer, CommentSerializer, LabelSerializer, \
    FolderSerializer, UserSerializer2
from rest_framework import generics
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator, available_attrs
from django.views.decorators.cache import cache_page, wraps


class PolygonList(generics.CreateAPIView):
    queryset = Polygon.objects.all()
    permission_classes = {IsAuthenticated, }
    serializer_class = PolygonSerializer

    def perform_create(self, serializer):
        user1 = User.objects.get(username=self.request.user)
        serializer.save(created_by=user1)


class CommentList(generics.CreateAPIView):
    permission_classes = {IsAuthenticated, }
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user1 = User.objects.get(username=self.request.user)
        serializer.save(created_by=user1)


class LabelList(generics.ListCreateAPIView):
    permission_classes = {IsAuthenticated, }
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


def cache_per_user(timeout):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            user_id = 'not_auth'
            if request.user.is_authenticated:
                user_id = request.user.id

            return cache_page(timeout, key_prefix="_user_{}_".format(user_id))(view_func)(request, *args, **kwargs)

        return _wrapped_view

    return decorator


class FolderList(generics.ListAPIView):
    serializer_class = FolderSerializer
    permission_classes = {IsAuthenticated, }

    def get_queryset(self):
        queryset = Folder.objects.filter(categories__allowed__username__contains=self.request.user).distinct()
        # for i in list(queryset):
        #     categories_list = i.categories.filter(allowed=self.request.user)
        #     if not categories_list:
        #         queryset.exclude(id=i.id)

        return queryset


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = {IsAuthenticated, }

    def get_queryset(self):
        try:
            folder = Folder.objects.get(id=self.kwargs.get('pk'))
        except Folder.DoesNotExist:
            raise Http404
        queryset = folder.categories.filter(allowed=self.request.user)

        return queryset


class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = {IsAuthenticated, }

    @method_decorator(cache_per_user(60000))
    def dispatch(self, *args, **kwargs):
        print("cached")
        return super(ImageList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        try:
            category = Category.objects.get(id=self.kwargs.get('pk'))
        except Category.DoesNotExist:
            raise Http404
        queryset = category.images.all()

        return queryset


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = {IsAuthenticated, }


class CommentsInImage(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            image = Image.objects.get(id=self.kwargs['pk'])
        except Image.DoesNotExist:
            raise Http404
        queryset = image.comments.filter(created_by=self.request.user)
        return queryset

    def get_serializer_class(self):
        return CommentSerializer


class PolygonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = {IsAuthenticated, }


class PolygonsInImage(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            image = Image.objects.get(id=self.kwargs['pk'])
        except Image.DoesNotExist:
            raise Http404
        queryset = image.polygons.filter(created_by=self.request.user)
        return queryset

    def get_serializer_class(self):
        return PolygonSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer2
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        serializer.save()
