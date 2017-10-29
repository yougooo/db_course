from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import *
from .plot_help import *
import psycopg2

def index(request):
    data_dict = {'p1':[], 'p2':[], 'p3':[],'p4':[]}
    date = []
    measurments_info = Measurments.objects.all()
    areas = Areas.objects.all()
    with connection.cursor() as cursor:
        cursor.execute('SELECT AVG(p1),AVG(p2),AVG(p3),AVG(p4) FROM measurments')
        stations = cursor.fetchall()

    for row in measurments_info:
        date.append(row.date)
        data_dict['p1'].append(row.p1)
        data_dict['p2'].append(row.p2)
        data_dict['p3'].append(row.p3)
        data_dict['p4'].append(row.p4)
    series = [make_series(val, date) for val in data_dict.values()]
    make_plots(series)
    context = {'info':measurments_info,'areas':areas,
                'zone_avg':stations}
    return render(request, 'index.html', context)





