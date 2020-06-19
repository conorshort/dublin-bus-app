from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS


# =================== SHAPE ===================

# ===== Shape Manager=====
class GTFSShapeManager(GTFSManager):

    def get_json_by_id(self, shape_id):
        ''' Take a shape_id and return a dict containing a list of its lats and'''
        shape = GTFSShape.objects.filter(shape_id=shape_id)
        num_points = len(shape)
        shape_dict = {"shape_id": shape[0].shape_id,
                      "points": [None] * num_points
                      }
        for point in shape:
            pt_seq = point.shape_pt_sequence
            shape_dict["points"][pt_seq - 1] = {"lat": point.shape_pt_lat,
                                                "lon": point.shape_pt_lon}
        return shape_dict


# ===== Shape Model =====
class GTFSShape(AbstractGTFS):
    unique_point_id = models.CharField(primary_key=True, max_length=70)
    shape_id = models.CharField(max_length=30)
    shape_pt_lat = models.FloatField(blank=True, null=True)
    shape_pt_lon = models.FloatField(blank=True, null=True)
    shape_pt_sequence = models.IntegerField()

    # Model manager
    objects = GTFSShapeManager()

    _text_file = "api/static/api/dublin_bus_gtfs/shapes.txt"

    def _proc_func(self, shape_dict):
        shape_dict["unique_point_id"] = f'{shape_dict["shape_id"]}:{shape_dict["shape_pt_sequence"]}'
        return shape_dict

    def __repr__(self):
        return f'''Id: {self.shape_id};
                   Coords: {self.shape_pt_lat}, {self.shape_pt_lon};
                   Seq: {self.shape_pt_sequence}'''

    class Meta:
        managed = True
        db_table = 'gtfs_shapes'
        unique_together = (("shape_id", "shape_pt_sequence"),)
