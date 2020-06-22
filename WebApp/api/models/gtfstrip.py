from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfsroute import GTFSRoute
from .gtfscalendar import GTFSCalendar
# =================== TRIPS ===================
class GTFSTrip(AbstractGTFS):
    route = models.ForeignKey(GTFSRoute, on_delete=models.CASCADE)
    calendar = models.ForeignKey(GTFSCalendar, on_delete=models.CASCADE)
    trip_id = models.CharField(primary_key=True, max_length=70)
    shape_id = models.CharField(max_length=70)
    trip_headsign = models.CharField(max_length=200)
    direction_id = models.IntegerField()

    _text_file = "trips.txt"

    class Meta:
        managed = True
        db_table = 'gtfs_trips'
