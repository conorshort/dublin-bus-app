from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfsagency import GTFSAgency

# =================== ROUTE ===================

class GTFSRoute(AbstractGTFS):
    route_id = models.CharField(primary_key=True, max_length=50)
    route_name = models.CharField(max_length=20)
    agency = models.ForeignKey(GTFSAgency, on_delete=models.CASCADE)

    _text_file = "routes.txt"

    def _dict_proc_func(self, route_dict, agency_dict):
        agency_id = agency_dict["id"]  
        route_dict["agency"] = GTFSAgency.objects.get(agency_id=agency_id)
        route_dict["route_name"] = route_dict["route_short_name"]
        return route_dict

    def __repr__(self):
        return self.route_id + " " + self.route_name

    class Meta:
        managed = True
        db_table = 'gtfs_routes'
