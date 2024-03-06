import uuid

from django.db import models
from django.db.models import Q

from .branch import Branch

class Printer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=20)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=False, null=False, related_name='printers')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = "printers"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(fields=['ip', 'branch'], name='unique_ip_branch'),
        ]

    def __str__(self):
        return '{}'.format(self.id)
