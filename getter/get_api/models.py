from django.db import models


# Create your models here.
class UploadFileModel(models.Model):
    file = models.FileField(upload_to="media")
    created_at = models.DateTimeField(auto_now_add=True)
