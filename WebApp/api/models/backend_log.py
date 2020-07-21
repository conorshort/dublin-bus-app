from django.db import models
from django.templatetags.static import static


class BackendLog(models.Model):
    date_time = models.DateField()
    file_name = models.CharField(max_length=128, blank=True, null=True)
    level_name = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'backend_log'
