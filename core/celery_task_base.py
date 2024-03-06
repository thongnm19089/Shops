import celery
from django.db import connection
from celery.utils.log import get_task_logger

from apps.marketings.models import CeleryTask

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    """ Implements after return hook to close the invalid connection.
    This way, django is forced to serve a new connection for the next
    task.
    """
    abstract = True

    def after_return(self, *args, **kwargs):
        try:
            CeleryTask.objects.filter(celery_task_id=self.request.id).update(is_done=True)
        except Exception as e:
            logger.error(f'error occurred: {e}')
        connection.close()
