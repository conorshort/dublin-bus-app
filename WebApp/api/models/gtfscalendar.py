from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfsagency import GTFSAgency
from datetime import datetime


class GTFSCalendar(AbstractGTFS):

    class Meta:
        managed = True
        db_table = 'gtfs_calendar'

    _text_file = "calendar.txt"

    agency = models.ForeignKey(GTFSAgency, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=128, primary_key=True)

    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()

    start_date = models.DateField()
    end_date = models.DateField()

    def _proc_func(self, calendar_dict, agency_dict):

        agency_id = agency_dict["id"]

        calendar_dict["agency"] = GTFSAgency.objects.get(agency_id=agency_id)

        calendar_dict["service_id"] = agency_id + \
            "_" + calendar_dict["service_id"]
 
        calendar_dict["start_date"] = datetime.strptime(
            calendar_dict["start_date"], "%Y%m%d")

        calendar_dict["end_date"] = datetime.strptime(
            calendar_dict["end_date"], "%Y%m%d")

        return calendar_dict
