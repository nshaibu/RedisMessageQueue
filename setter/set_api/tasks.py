import time
import redis
from django.core.files.storage import default_storage
from django.conf import settings
from celery.utils.log import get_task_logger
from setter.celery import app


logger = get_task_logger(__name__)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@app.task(name="process_file")
def process_file(file_name):
    fd = default_storage.open(file_name, "r")
    content = fd.readlines()
    redis_instance.publish(settings.REDIS_CHANNEL, f"FILE_NAME:{file_name}")
    for line in content:
        redis_instance.publish(settings.REDIS_CHANNEL, line)
        print(line)
        time.sleep(1.0/20)
    redis_instance.publish(settings.REDIS_CHANNEL, "CLOSE_FILE")
    fd.close()

