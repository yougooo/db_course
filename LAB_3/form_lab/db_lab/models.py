from __future__ import unicode_literals
from django.contrib.gis.db import models



class Areas(models.Model):
    short_n = models.CharField(primary_key=True, max_length=10)
    full_n = models.CharField(max_length=255)


    def __str__(self):
        return self.short_n

    class Meta:
        managed = True
        db_table = 'areas'



class StationRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    station_type = models.CharField(unique=True, max_length=255, blank=True, null=True)
    p7_value = models.FloatField(unique=True, blank=True, null=True)


    def __str__(self):
        return str(self.station_type)

    class Meta:
        managed = False
        db_table = 'station_role'



class Stations(models.Model):
    area = models.ForeignKey(Areas, models.CASCADE, db_column='area', blank=True, null=True)
    station = models.SmallIntegerField()
    station_id = models.AutoField(primary_key=True)
    point_x = models.FloatField()
    point_y = models.FloatField()
    point_z = models.FloatField()
    role = models.ForeignKey(StationRole, models.CASCADE, db_column='role', blank=True, null=True)

    def __str__(self):
        return str(self.area)+'_'+str(self.station)

    class Meta:
        managed = True
        db_table = 'stations'
        unique_together = (('station','area'))



class Measurments(models.Model):
    date = models.DateField()
    time = models.TimeField()
    base_station = models.ForeignKey('Stations', models.CASCADE, db_column='base_station')
    p1 = models.FloatField(blank=True)
    p2 = models.SmallIntegerField(blank=True)
    p3 = models.SmallIntegerField(blank=True)
    p4 = models.FloatField(blank=True)
    p7 = models.FloatField(blank=True, null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.base_station)

    class Meta:
        managed = True
        db_table = 'measurments'
        unique_together = (('date', 'time', 'base_station'),)



