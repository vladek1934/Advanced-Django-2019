"""Week2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from base import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token),
    path('register/', views.RegisterUserAPIView.as_view()),
    path('api/token/', obtain_jwt_token, name='api_token_auth'),
    path('blocks/', views.BlockList.as_view()),
    path('blocks/<int:pk>/', views.BlockDetail.as_view()),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
router = DefaultRouter()
router.register('profiles', ProfileViewSet, base_name='profiles')
router.register('projects', ProjectViewSet, base_name='projects')
router.register('members', ProjectMemberViewSet, base_name='members')
# router.register('blocks', BlockViewSet, base_name='blocks')
router.register('tasks', TaskViewSet, base_name='tasks')
router.register('documents', DocumentViewSet, base_name='documents')
router.register('comments', CommentViewSet, base_name='comments')

urlpatterns += router.urls
