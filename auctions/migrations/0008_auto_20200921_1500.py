# Generated by Django 3.1.1 on 2020-09-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200920_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
