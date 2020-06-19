from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS

# =================== TRIPS ===================
class GTFSTrip(AbstractGTFS):
    route_id = models.CharField(max_length=70)
    service_id = models.CharField(max_length=70)
    trip_id = models.CharField(primary_key=True, max_length=70)
    shape_id = models.CharField(max_length=70)
    trip_headsign = models.CharField(max_length=200)
    direction_id = models.IntegerField()

    _text_file = "api/static/api/dublin_bus_gtfs/trips.txt"

    class Meta:
        managed = True
        db_table = 'gtfs_trips'
