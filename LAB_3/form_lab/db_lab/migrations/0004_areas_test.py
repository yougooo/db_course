# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_lab', '0003_auto_20171023_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='areas',
            name='test',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]