from django.db import models
from django.templatetags.static import static

# ========================================================================================
# ========================================================================================
# Models to store the GTFS data found here https://transitfeeds.com/p/transport-for-ireland/782/latest


# =================== Manager for all GTFS classes ===================
# Includes a method that will read from a class's associated
# text files and add it to the db. Can be called with
# <gtfs-class>.objects.update_all()
class GTFSManager(models.Manager):

    def update_all(self):
        ''' Read data from a text file and import to mysql
        The text files are found as a class variable in each GTFS class'''
        import pandas as pd
        self.all().delete()
        for agency_dict in self.model._agencies:
            text_file = agency_dict["path"] + self.model._text_file
            print("Getting data from", text_file)
            df = pd.read_csv(text_file)
            df_records = df.to_dict('records')

            print("Creating instances...")

            model_instances = []
            for i, record in enumerate(df_records):
                gtfs_instance = self.model.from_dict(record, agency_dict)
                model_instances.append(gtfs_instance)
                if i % 10000 == 0:
                    print(f"Adding entries up to {i} to db...")
                    self.bulk_create(model_instances)
                    model_instances = []
            self.bulk_create(model_instances)
        print("Done")


class AbstractGTFS(models.Model):
    ''' Abstract class that all GTFS classes inherit from
    Sets the model manager for each class to GTFSManager'''
    objects = GTFSManager()

    class Meta:
        abstract = True

    _agencies = [{"name": "Dublin Bus",
                 "id": "978",
                 "path": "api/static/api/dublin_bus_gtfs/"},
                {"name": "Go Ahead",
                 "id": "03",
                 "path": "api/static/api/go_ahead_gtfs/"}, ]

    @classmethod
    def from_dict(cls, gtfs_dict, agency_dict):
        ''' Create an instance of a class from a dictionary
        If a class includes a _proc_func runs the dictionary
        throught that first '''

        # Create an instance of the class
        gtfs_instance = cls()

        # Alter the dictionary with _proc_func if found
        proc_func = getattr(gtfs_instance, "_proc_func", None)
        if proc_func:
            gtfs_dict = proc_func(gtfs_dict, agency_dict)

        # Loop through the dict and set the instance values
        for key, val in gtfs_dict.items():
            if key in dir(gtfs_instance):
                setattr(gtfs_instance, key, val)
        return gtfs_instance
