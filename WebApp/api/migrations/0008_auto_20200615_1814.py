# Generated by Django 3.0.3 on 2020-06-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200615_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gtfsstoptime',
            name='unique_trip_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='gtfstrip',
            name='route_id',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='gtfstrip',
            name='service_id',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='gtfstrip',
            name='shape_id',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='gtfstrip',
            name='trip_id',
            field=models.CharField(max_length=70, primary_key=True, serialize=False),
        ),
    ]
