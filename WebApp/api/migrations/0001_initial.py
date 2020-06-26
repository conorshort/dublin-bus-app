# Generated by Django 3.0.3 on 2020-06-23 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GTFSAgency',
            fields=[
                ('agency_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('agency_name', models.CharField(max_length=255, unique=True)),
                ('agency_url', models.URLField()),
                ('agency_timezone', models.CharField(max_length=64)),
                ('agency_lang', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'db_table': 'gtfs_agency',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GTFSCalendar',
            fields=[
                ('service_id', models.CharField(max_length=128)),
                ('agency_service_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('monday', models.BooleanField()),
                ('tuesday', models.BooleanField()),
                ('wednesday', models.BooleanField()),
                ('thursday', models.BooleanField()),
                ('friday', models.BooleanField()),
                ('saturday', models.BooleanField()),
                ('sunday', models.BooleanField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSAgency')),
            ],
            options={
                'db_table': 'gtfs_calendar',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GTFSRoute',
            fields=[
                ('route_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('route_name', models.CharField(max_length=20)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSAgency')),
            ],
            options={
                'db_table': 'gtfs_routes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GTFSStop',
            fields=[
                ('stop_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('stop_name', models.CharField(max_length=1024)),
                ('stop_lat', models.FloatField()),
                ('stop_lon', models.FloatField()),
            ],
            options={
                'db_table': 'gtfs_stops',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SmartDublinBusStop',
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
                'db_table': 'sd_bus_stops',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GTFSTrip',
            fields=[
                ('trip_id', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('shape_id', models.CharField(max_length=70)),
                ('trip_headsign', models.CharField(max_length=200)),
                ('direction_id', models.IntegerField()),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSCalendar')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSRoute')),
            ],
            options={
                'db_table': 'gtfs_trips',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GTFSStopTime',
            fields=[
                ('unique_trip_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('arrival_time', models.IntegerField(blank=True, null=True)),
                ('departure_time', models.IntegerField(blank=True, null=True)),
                ('stop_sequence', models.IntegerField()),
                ('stop_headsign', models.CharField(max_length=200)),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSStop')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSTrip')),
            ],
            options={
                'db_table': 'gtfs_stop_times',
                'managed': True,
            },
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
        migrations.CreateModel(
            name='GTFSCalendarDate',
            fields=[
                ('service_id', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('exception_type', models.IntegerField()),
                ('unique_calendar_date_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GTFSCalendar')),
            ],
            options={
                'db_table': 'gtfs_calendar_dates',
                'managed': True,
            },
        ),
    ]
