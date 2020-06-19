from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS

# =================== ROUTE ===================

class GTFSRoute(AbstractGTFS):
    route_id = models.CharField(primary_key=True, max_length=50)
    route_name = models.CharField(max_length=20)

    _text_file = "api/static/api/dublin_bus_gtfs/routes.txt"

    def _proc_func(self, route_dict):
        route_dict["route_name"] = route_dict["route_short_name"]
        return route_dict

    def __repr__(self):
        return self.route_id + " " + self.route_name

    objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'gtfs_routes'
