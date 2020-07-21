from django.db import models
from django.templatetags.static import static
from django.utils import timezone

class BackendLog(models.Model):
    date_time = models.DateTimeField()
    file_name = models.CharField(max_length=128, blank=True, null=True)
    level_name = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'backend_log'

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_time = timezone.now()

        return super(BackendLog, self).save(*args, **kwargs)
