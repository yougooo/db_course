from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from excel_response2 import ExcelResponse
from .models import *


class AdminAreas(admin.ModelAdmin):
    list_display = ['short_n', 'full_n']
    ordering = ['short_n']


class AdminMeasurments(admin.ModelAdmin):
    list_display = ['id','date','time','station','area','p1','p2','p3','p4']
    ordering = ['id']
    actions = ['export_excel']
    def export_excel(modeladmin, request, queryset):
        for i in queryset:
            print(i)
        return ExcelResponse(queryset)


class AdminStations(admin.ModelAdmin):
    list_display = ['area','station','point_x','point_y','point_z']

admin.site.register(Areas, AdminAreas)
admin.site.register(Measurments, AdminMeasurments)
admin.site.register(Stations, AdminStations)


