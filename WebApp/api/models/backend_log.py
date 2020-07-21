from django.db import models

class BackendLog(models.Manager):
    date_time = models.DateField()
    file_name = models.CharField(max_length=128)
    level_name = models.CharField(max_length=128)
    message = models.TextField()

    class Meta:
        managed = True
        db_table = 'backend_log'
