<p>Tasks: </p>
<p>1. Створіть прості форми для всіх таблиць вашої бази даних. Перевірте їх
працездатність вводячи нові дані через форму, використовуючи датасет
DB_Lab2_Data.xls. Занотуйте помилки імпорту, поясніть їх причину.</p>
<p>2. Використовуючи раніше створену базу даних, створіть наступні запити з
агрегатними функціями:</p>
<p>1) Вивести середнє значення вимірюваних параметрів Р* за окремими
станціям спостереження.;</p>
<p>2) Узагальніть попередній запит, виводячи середні значення тих же
параметрів в межах площ;</p>
<p>3. Створіть звіти, використовуючи прості запити із роботи №1 та перехресні
запити із роботи №2 (скориставшись рівнями групування по відповідним
полям).</p>

<p>First of all check <a href="https://wiki.postgresql.org/wiki/Community_Guide_to_PostgreSQL_GUI_Tools">postgresql wiki</a> here we can find few gui tools for task_1, but almost all have some bag, or have't support on Linux.</p>

<p>For me more common way for form it some client in web and some back-end in server side with our data base. We use form very often, for example when loggined in social network, or do online shopping, etc.</p>

<p>Simple way to start develop in web use some RAD(Rational Application Developet) framework, I am familiar with Django.</p>
<p>In general almost all work was done, before we starting developed, partly because it common pattern, partly because it's Django('all inclusive'). Ofcouse we need write more custom logic, more validation for form, more test, but not now. Now just minimum work prototype. </p>
<p>First step after we start our Django app its connect app to our database(from LAB_1)</p>

```python
#./form_lab/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lab_1',
        'USER': 'alex',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
```
<p>Next step, we need way to work with data from table in database in our app. In MVT model its is Model level, if say shortly we define one model per table in special file models.py. After model will be define we may interact with data through ORM(Object-relational mapping) object Django</p>
<p>We already have database, so we may use some django useful staff:</p>

```terminal
python manage.py inspectdb > ./db_lab/models.py
```
<p>After this command we have file with automatic generated models from database. Some correction and we have this:</p>

```python
#./db_lab/models.py
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
```
<p>Ofcouse it is not best practice in model(not 'fat'), but it is okey for our task.</p>
<p>Now we may go to setup forms. Django already have admin panel. So all we need to do for get our model in admin panel, just register model in special file admin.py.</p>

```python
/db_lab/admin.py
class AdminAreas(admin.ModelAdmin):
    list_display = ['short_n', 'full_n']
    ordering = ['short_n']

class AdminMeasurments(admin.ModelAdmin):
    list_display = ['id','date','time','station','area','p1','p2','p3','p4']
    ordering = ['id'] 
    actions = ['export_excel'] # came soon

class AdminStations(admin.ModelAdmin):
    list_display = ['area','station','point_x','point_y','point_z']

admin.site.register(Areas, AdminAreas)
admin.site.register(Measurments, AdminMeasurments)
admin.site.register(Stations, AdminStations)
```
<p>create user why take control</p>

```terminal
python manage.py createsuperuser
```
<p>That's all we need for take admin control under data in Django app. Some screenshot how it is look like</p>

![alt text](https://github.com/yougooo/db_course/blob/master/LAB_2/Screenshot%20from%202017-10-02%2002-43-46.png)

<p></p>

![alt text](https://github.com/yougooo/db_course/blob/master/LAB_2/Screenshot%20from%202017-10-02%2002-44-38.png)

<p></p>

![alt text](https://github.com/yougooo/db_course/blob/master/LAB_2/Screenshot%20from%202017-10-02%2002-44-57.png)

<p></p>

![alt text](https://github.com/yougooo/db_course/blob/master/LAB_2/Screenshot%20from%202017-10-02%2002-45-25.png)

<p>For task_2 I used code in views.py, so in MVT model it is View level and here we define logic for our data, write some functions wich wating for user request and after this do some usful action with data and return result for user.</p>

```python
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
```

<p>So, here we have super-simple view(function based) called 'index'. After user call this function data from our model come to view, next we pass this data in spetial template, where html page rendering wiht data and return like response.</p>
<p>Table screenshot:</p>

![alt text](https://github.com/yougooo/db_course/blob/master/LAB_2/Screenshot%20from%202017-10-02%2003-19-27.png)

![alt text](https://github.com/yougooo/db_course/blob/master/LAB_2/Screenshot%20from%202017-10-02%2003-19-45.png)

