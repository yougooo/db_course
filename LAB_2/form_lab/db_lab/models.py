from __future__ import unicode_literals
from django.contrib.gis.db import models


class Areas(models.Model):
    short_n = models.CharField(primary_key=True, max_length=10)
    full_n = models.CharField(max_length=255)

    def __str__(self):
        return self.full_n

    class Meta:
        managed = True
        db_table = 'areas'


class Stations(models.Model):
    area = models.ForeignKey(Areas, models.CASCADE, db_column='area')
    station = models.SmallIntegerField(primary_key=True)
    point_x = models.FloatField()
    point_y = models.FloatField()
    point_z = models.FloatField()


    def __str__(self):
        return str(self.station)


    class Meta:
        managed = True
        db_table = 'stations'
        unique_together = (('station', 'area'),)


class Measurments(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(primary_key=True)
    time = models.TimeField()
    area = models.ForeignKey(Areas, models.CASCADE, db_column='area')
    station = models.ForeignKey(Stations, models.CASCADE, db_column='station')
    p1 = models.FloatField()
    p2 = models.SmallIntegerField()
    p3 = models.SmallIntegerField()
    p4 = models.FloatField()

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True
        db_table = 'measurments'
        unique_together = (('date', 'time', 'area', 'station', 'id'),)



