from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfscalendar import GTFSCalendar
from datetime import datetime


class GTFSCalendarDate(AbstractGTFS):

    class Meta:
        managed = True
        db_table = 'gtfs_calendar_dates'

    _text_files = "calendar_dates.txt"

    calendar = models.ForeignKey(GTFSCalendar, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=128)
    date = models.DateField()
    exception_type = models.IntegerField()

    def _proc_func(self, calendar_date_dict, agency_dict):

        agency_id = agency_dict["id"]

        calendar_date_dict["service_id"] = agency_id + \
            "_" + calendar_date_dict["service_id"]

        calendar_date_dict["calendar"] = GTFSAgency.objects.get(
            service_id=calendar_date_dict["service_id"])

        calendar_date_dict["date"] = datetime.strptime(
            calendar_date_dict["date"], "%Y%m%d")

        return calendar_date_dict
