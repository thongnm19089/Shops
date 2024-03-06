import os

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.deconstruct import deconstructible
# from apps.products.models import Product


@deconstructible
class UploadTo:
    def __init__(self, model, field):
        self.model = model
        self.field = field

    def __eq__(self, other):
        return self.model == other.model and self.field == other.field

    def __call__(self, instance, filename):
        model_pk = instance.product.pk if hasattr(instance, 'product') else instance.pk
        return os.path.join(
            self.model,
            self.field,
            str(model_pk),
            filename
        )


class CustomManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        for i in objs:
            pre_save.send(type(i), instance=i, created=True)
        super().bulk_create(objs, **kwargs)
        for i in objs:
            post_save.send(type(i), instance=i, created=True)

    def bulk_update(self, objs, fields, **kwargs):
        for i in objs:
            pre_save.send(type(i), instance=i, created=False)
        super().bulk_update(objs, fields, **kwargs)
        for i in objs:
            post_save.send(type(i), instance=i, created=False)


def get_model_attribute(instance, field):
    if not field:
        return None
    fields = field.split(".", 1)
    attr = None
    if getattr(instance, fields[0], None):
        attr = getattr(instance, fields[0])
    if len(fields) > 1:
        temp = get_model_attribute(attr, fields[1])
        if temp:
            attr = temp
    return attr


class CustomDateTimeField(models.DateTimeField):
    def __init__(self, verbose_name=None, name=None, auto_now=False,
                 auto_now_add=False, **kwargs):
        super().__init__(verbose_name, name, auto_now, auto_now_add, **kwargs)

    def pre_save(self, model_instance, add):
        force_value = getattr(model_instance, self.attname)
        if force_value is None:
            return super(CustomDateTimeField, self).pre_save(model_instance, add)
        return force_value
