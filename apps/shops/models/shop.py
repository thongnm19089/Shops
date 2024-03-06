import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from core.models import UploadTo


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    slug_name = models.SlugField(max_length=100, blank=True, null=True)
    slug_name_index = models.PositiveIntegerField(blank=True, null=True, default=0)
    address = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    dayoff_allowed = models.PositiveIntegerField(blank=True, null=True, default=2)
    hotline = models.CharField(max_length=15, blank=True, null=True)
    logo_url = models.FileField(
        upload_to=UploadTo("shops", "logo"),
        max_length=1024,
        blank=True,
        null=True,
    )
    copyright = models.TextField(blank=True, null=True)
    owner_info = models.TextField(blank=True, null=True)
    landing_page_title = models.CharField(max_length=100, blank=True, null=True)
    website_url = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shop"
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        new_slug_name = slugify(self.name)
        if new_slug_name != self.slug_name:
            last_object = (
                Shop.objects.filter(slug_name=new_slug_name)
                      .order_by('-slug_name_index').first()
            )
            if not last_object:
                index = 1
            else:
                index = last_object.slug_name_index + 1
            self.slug_name = new_slug_name
            self.slug_name_index = index
        super(Shop, self).save(*args, **kwargs)
