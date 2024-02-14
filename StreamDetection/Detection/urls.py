from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("video", views.playvideo, name = "video"),
    path("upload", views.upload_file, name = "upload")

]