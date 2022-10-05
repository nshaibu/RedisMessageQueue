import time
import redis
from io import BytesIO
from django.conf import settings
from django.core.files.base import File
from celery.utils.log import get_task_logger

from getter.celery import app
from get_api.models import UploadFileModel
from celery.contrib import rdb


logger = get_task_logger(__name__)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@app.task(name="create_file")
def create_file():
    pubsub = redis_instance.pubsub()
    pubsub.subscribe(settings.REDIS_CHANNEL)
    fd = None
    file_name = None
    while True:
        message = pubsub.get_message()
        if message:
            print(message)
            data = message['data']
            data_str = data.decode() if isinstance(data, bytes) else str(data)
            command = data_str.split(':')[0]
            if command == "FILE_NAME":
                file_name = data_str.split(":")[1]
                if file_name:
                    fd = BytesIO()
            elif command == "CLOSE_FILE" and fd:
                img_bytes = fd.getvalue()
                logger.info(img_bytes)
                instance = UploadFileModel.objects.create()
                instance.file.save(file_name, File(fd))
                fd.close()
                fd = None
                file_name = None
            else:
                if fd:
                    if not isinstance(data, bytes):
                        data = str(data).encode()
                    fd.write(data)
        time.sleep(1.0 / 20)

