import uuid

from django.db import models
from django.db.models import Q
import slugify
from .shop import Shop


class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    slug_name = models.SlugField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    root_branch = models.BooleanField(blank=False, null=False, default=False)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "branch"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_branch_name'),
        ]

    def save(self, *args, **kwargs):
        self.slug_name = slugify.slugify(self.name)
        super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return '{}-{}'.format(self.name, self.address)
