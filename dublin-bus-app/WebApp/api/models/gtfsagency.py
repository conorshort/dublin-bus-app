from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS


# Agency: contains name and id of each company (id dublin bus, go ahead)
class GTFSAgency(AbstractGTFS):

    class Meta:
        managed = True
        db_table = 'gtfs_agency'

    agency_id = models.CharField(max_length=128, primary_key=True)
    agency_name = models.CharField(max_length=255, unique=True)
    agency_url = models.URLField()
    agency_timezone = models.CharField(max_length=64)
    agency_lang = models.CharField(max_length=2, null=True, blank=True)
    
    _text_file = "agency.txt"
