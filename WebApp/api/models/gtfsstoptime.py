from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfstrip import GTFSTrip
from .gtfsstop import GTFSStop
# =================== STOP TIMES ===================

class GTFSStopTime(AbstractGTFS):
    unique_trip_id = models.CharField(primary_key=True, max_length=50)
    trip = models.ForeignKey(GTFSTrip, on_delete=models.CASCADE)
    arrival_time = models.IntegerField(blank=True, null=True)
    departure_time = models.IntegerField(blank=True, null=True)
    stop = models.ForeignKey(GTFSStop, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=200)

    _text_file = "stop_times.txt"

    def __time_to_secs(self, time):
        hrs, mins, secs = time.split(":")
        hrs_to_secs = int(hrs) * 3600
        mins_to_secs = int(mins) * 60
        return hrs_to_secs + mins_to_secs + int(secs)

    def _dict_proc_func(self, stop_time_dict, agency_dict):
        # Make unique trip id as primary key
        stop_time_dict["unique_trip_id"] = f'{stop_time_dict["trip_id"]}:{stop_time_dict["stop_sequence"]}'

        stop_time_dict["trip"] = GTFSTrip(trip_id=stop_time_dict["trip_id"])

        stop_time_dict["stop"] = GTFSStop(stop_id=stop_time_dict["stop_id"])

        # Convery dept and arr time to secs after midnight
        stop_time_dict["arrival_time"] = self.__time_to_secs(
            stop_time_dict["arrival_time"])
        stop_time_dict["departure_time"] = self.__time_to_secs(
            stop_time_dict["departure_time"])

    
        return stop_time_dict


    class Meta:
        managed = True
        db_table = 'gtfs_stop_times'
