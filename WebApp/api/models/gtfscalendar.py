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
    service_id = models.CharField(max_length=128)
    agency_service_id = models.CharField(max_length=128, primary_key=True)

    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()

    start_date = models.DateField()
    end_date = models.DateField()

    display_days = models.CharField(max_length=128, blank=True, null=True)

    def _dict_proc_func(self, calendar_dict, agency_dict):

        agency_id = agency_dict["id"]

        # The service ids agencies use might overlap, to fix this
        # append the agency id to the start to get a unique id
        calendar_dict["agency_service_id"] = agency_id + \
            "_" + calendar_dict["service_id"]

        # Get the correct agency from the db
        calendar_dict["agency"] = GTFSAgency.objects.get(agency_id=agency_id)
    
        # Make start and end date into date time objects
        calendar_dict["start_date"] = datetime.strptime(
            str(calendar_dict["start_date"]), "%Y%m%d")

        calendar_dict["end_date"] = datetime.strptime(
            str(calendar_dict["end_date"]), "%Y%m%d")

        return calendar_dict
