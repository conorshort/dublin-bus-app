from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS

# =================== ROUTE ===================


class GTFSStop(AbstractGTFS):
    stop_id = models.CharField(max_length=128, primary_key=True)
    stop_name = models.CharField(max_length=1024)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()

    _text_file = "stops.txt"

    class Meta:
        managed = True
        db_table = 'gtfs_stops'
