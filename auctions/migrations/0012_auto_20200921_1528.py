# Generated by Django 3.1.1 on 2020-09-21 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200921_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
