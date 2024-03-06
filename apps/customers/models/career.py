from django.db import models

class Career(models.Model):
    name = models.CharField(max_length=50, unique=True)