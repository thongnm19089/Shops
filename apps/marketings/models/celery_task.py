import uuid

from django.db import models


class CeleryTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    celery_task_id = models.CharField(max_length=50)
    content = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "celery_task"
        ordering = ["-created_at"]
        
    def __str__(self):
        return '{}'.format(self.id)
    