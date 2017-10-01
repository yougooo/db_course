from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import *
import psycopg2 

def index(request):
    measurments_info = Measurments.objects.all()
    areas = Areas.objects.all()
    with connection.cursor() as cursor:
        cursor.execute('SELECT station, AVG(p1),AVG(p2),AVG(p3),AVG(p4) FROM measurments GROUP BY station')
        by_stations = cursor.fetchall()
        cursor.execute('SELECT area, AVG(p1),AVG(p2),AVG(p3),AVG(p4) FROM measurments GROUP BY area')
        by_areas = cursor.fetchall()

    context = {'info':measurments_info,'areas':areas,
                'zone_avg':by_stations, 'area_avg':by_areas}
    return render(request, 'index.html', context)


    
                                 

