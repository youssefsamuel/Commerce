# Generated by Django 3.1.1 on 2020-09-21 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200921_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='desciption',
            new_name='description',
        ),
    ]
