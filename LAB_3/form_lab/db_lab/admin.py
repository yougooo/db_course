from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from excel_response2 import ExcelResponse
from django.contrib.contenttypes.models import ContentType
from .models import *

def export_selected(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHEKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("export/?ct={}&ids=()".format(ct.pk,
                                                              ','.join(selected)))


admin.site.add_action(export_selected, 'export_selected')


class AdminAreas(admin.ModelAdmin):
    list_display = ['short_n', 'full_n']
    ordering = ['short_n']


class AdminMeasurments(admin.ModelAdmin):
    list_display = ['id','date','time','base_station','checked','p1','p2','p3','p4','p7']
    actions = ['export_selected', 'checked', 'set_p7']


    def checked(self, request, queryset):
        rows_update = queryset.update(checked=True)
        self.message_user(request,'{} row(s) successfully marked as checked.'.format(rows_update))

    def set_p7(self, reqyest, queryset):
        for query in queryset:
            print(str(query))



class AdminStations(admin.ModelAdmin):
    list_display = ['station_id','area','station','role','point_x','point_y','point_z']
    actions = ['set_main', 'set_minor']


    def set_main(self,request,queryset):
        rows_update = queryset.update(role=1)
        self.message_user(request,'{} row(s) successfully marked as main.'.format(rows_update))

    def set_minor(self,request,queryset):
        rows_update = queryset.update(role=2)
        self.message_user(request,'{} row(s) successfully marked as minor.'.format(rows_update))



admin.site.register(Areas, AdminAreas)
admin.site.register(Measurments, AdminMeasurments)
admin.site.register(Stations, AdminStations)

