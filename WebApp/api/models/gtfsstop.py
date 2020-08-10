from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS

# =================== ROUTE ===================


class GTFSStop(AbstractGTFS):
    stop_id = models.CharField(max_length=128, primary_key=True)
    stop_name = models.CharField(max_length=1024)
    plate_code = models.CharField(max_length=20, blank=True, null=True)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    # sd_stop = models.ForeignKey(SmartDublinBusStop, on_delete=models.CASCADE)

    _text_file = "stops.txt"

    def _dict_proc_func(self, stops_dict, agency_dict):
        try:
            stop_name, stop_plate_code = stops_dict["stop_name"].split(", stop ")
        except e:
            stop_name = stops_dict["stop_name"]
            stop_plate_code = None
        stops_dict["stop_name"] = stop_name
        stops_dict["plate_code"] = stop_plate_code
        return stops_dict

    class Meta:
        managed = True
        db_table = 'gtfs_stops'
