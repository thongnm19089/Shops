from django.db import models

class ActiveCode(models.Model):
    code = models.CharField(max_length=10)
    user_id = models.UUIDField()
    
    class Meta:
        db_table = 'active_code'
