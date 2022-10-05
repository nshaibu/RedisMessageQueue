from django.urls import path

from . import views

app_name = "get_api"

urlpatterns = [
    path('', views.ListFilesView.as_view(), name="list_all_files")
]