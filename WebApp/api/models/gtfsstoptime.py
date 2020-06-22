from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfstrip import GTFSTrip

# =================== STOP TIMES ===================

class GTFSStopTime(AbstractGTFS):
    unique_trip_id = models.CharField(primary_key=True, max_length=50)
    trip = models.ForeignKey(GTFSTrip, on_delete=models.CASCADE)
    arrival_time = models.IntegerField(blank=True, null=True)
    departure_time = models.IntegerField(blank=True, null=True)
    stop_id = models.CharField(max_length=50)
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=200)

    _text_file = "stop_times.txt"

    def __time_to_secs(self, time):
        hrs, mins, secs = time.split(":")
        hrs_to_secs = int(hrs) * 3600
        mins_to_secs = int(mins) * 60
        return hrs_to_secs + mins_to_secs + int(secs)

    def _proc_func(self, calendar_date_dict, textfile):
        stop_time_dict["unique_trip_id"] = f'{stop_time_dict["trip_id"]}:{stop_time_dict["stop_sequence"]}'
        stop_time_dict["arrival_time"] = self.__time_to_secs(
            stop_time_dict["arrival_time"])
        stop_time_dict["departure_time"] = self.__time_to_secs(
            stop_time_dict["departure_time"])
        return stop_time_dict

    class Meta:
        managed = True
        db_table = 'gtfs_stop_times'
