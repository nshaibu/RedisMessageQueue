import redis
from django.views import generic
from django.conf import settings
from get_api.tasks import create_file
from get_api.models import UploadFileModel

CELERY = {}


class ListFilesView(generic.ListView):
    template_name = "getter_api/files_view.html"
    queryset = UploadFileModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not CELERY:
            CELERY['id'] = create_file.delay().task_id
        return context

