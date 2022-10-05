from django.urls import path

from . import views

app_name = "set_api"

urlpatterns = [
    path('', views.UploadFileView.as_view(), name="upload_file"),
]
