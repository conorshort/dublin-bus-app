# Generated by Django 3.0.3 on 2020-06-16 14:07

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('stopid', models.IntegerField(primary_key=True, serialize=False)),
                ('shortnamelocalized', models.CharField(blank=True, max_length=200, null=True)),
                ('fullname', models.CharField(blank=True, max_length=200, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('lastupdated', models.DateField(blank=True, null=True)),
                ('routes', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bus_stops',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GTFSRoute',
            fields=[
                ('route_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('route_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'gtfs_routes',
                'managed': True,
            },
            managers=[
                ('updater', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GTFSStopTime',
            fields=[
                ('unique_trip_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('trip_id', models.CharField(max_length=50)),
                ('arrival_time', models.IntegerField(blank=True, null=True)),
                ('departure_time', models.IntegerField(blank=True, null=True)),
                ('stop_id', models.CharField(max_length=50)),
                ('stop_sequence', models.IntegerField()),
                ('stop_headsign', models.CharField(max_length=200)),

            ],
            options={
                'db_table': 'gtfs_stop_times',
                'managed': True,
            },
            managers=[
                ('updater', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GTFSTrip',
            fields=[
                ('route_id', models.CharField(max_length=70)),
                ('service_id', models.CharField(max_length=70)),
                ('trip_id', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('shape_id', models.CharField(max_length=70)),
                ('trip_headsign', models.CharField(max_length=200)),
                ('direction_id', models.IntegerField()),
            ],
            options={
                'db_table': 'gtfs_trips',
                'managed': True,
            },
            managers=[
                ('updater', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GTFSShape',
            fields=[
                ('unique_point_id', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('shape_id', models.CharField(max_length=30)),
                ('shape_pt_lat', models.FloatField(blank=True, null=True)),
                ('shape_pt_lon', models.FloatField(blank=True, null=True)),
                ('shape_pt_sequence', models.IntegerField()),
            ],
            options={
                'db_table': 'gtfs_shapes',
                'managed': True,
                'unique_together': {('shape_id', 'shape_pt_sequence')},
            },
        ),
    ]