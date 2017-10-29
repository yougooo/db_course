# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 08:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_lab', '0002_auto_20171021_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station_role',
            fields=[
                ('type', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='stations',
            name='role',
            field=models.ForeignKey(blank=True, db_column='station_role', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_lab.Station_role'),
        ),
    ]
