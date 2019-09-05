from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('polygon/', views.PolygonList.as_view()),  # Add polygons
    path('folders/<int:pk>/', views.CategoryList.as_view()),  # List image categories at a folder PK
    path('polygon/<int:pk>/', views.PolygonDetail.as_view()),  # Delete polygon at PK
    path('images/<int:pk>/', views.ImageList.as_view()),  # Show images in category PK
    path('image/<int:pk>/polygons/', views.PolygonsInImage.as_view()),  # Show polygons in image PK
    path('comment/', views.CommentList.as_view()),  # Add comments
    path('comment/<int:pk>/', views.CommentDetail.as_view()),  # Delete/show comment at PK
    path('image/<int:pk>/comments/', views.CommentsInImage.as_view()),  # Show comments in image PK
    path('analytics/<int:pk>/', views.FullAnalytics2.as_view()),  # gives out a link to the pdf
    path('labels/', views.LabelList.as_view()),  # lists labels
    path('folders/', views.FolderList.as_view()),
    path('register/', views.UserRegister.as_view())
    # show folders to a user. Does not show a folder which is empty/all of the contents are invisible.

]

# path('', FileUploadView.as_view())
# path('image/<int:imageId>/analytics/', views.UserImageAnalytics.as_view()),
# path('image/<int:imageId>/analytics/all/', views.ImageAnalytics.as_view()),
# path('myanalytics/', views.UserAnalytics.as_view()),
