import uuid

from django.db import models
from django.db.models import Q


class Shift(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()
    flexible_minutes = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = "shift"
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_shift_name"
            ),
        ]
        ordering = ["created_at"]
