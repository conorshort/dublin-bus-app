# Generated by Django 3.0.3 on 2020-06-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gtfscalendar',
            name='calendar_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
