# Generated by Django 3.0.3 on 2020-06-11 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routeplanner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StopSequence',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('shape_id', models.CharField(max_length=30)),
                ('operator', models.CharField(max_length=50)),
                ('stop_sequence', models.IntegerField()),
                ('route_name', models.CharField(max_length=10)),
                ('direction_inbound', models.BooleanField()),
                ('plate_code', models.IntegerField()),
                ('short_common_name_en', models.CharField(max_length=100)),
                ('short_common_name_ga', models.CharField(max_length=100)),
                ('has_pole', models.BooleanField()),
                ('has_shelter', models.BooleanField()),
                ('carousel_type', models.CharField(max_length=100)),
                ('flag_data', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'stopsequences',
                'managed': True,
                'unique_together': {('shape_id', 'stop_sequence')},
            },
        ),
    ]