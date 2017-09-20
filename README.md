# db_course
<h3>Lab_1</h3>
From excel file DB_Lab1_Data.xls we going to create database in PostgreSQL. For import data in our database we can use several way:
<p> - use pgadmin III, creat table with GUI, then copy/past values from spreadsheet, but it is to long and come with a lot of rutine misteke;</p>
<p> - save eche spreadsheet like .csv file, then import with psql comand '\copy' and work in pgadmin III, it is okey, but we may have some truble with type convert;</p>
<p> - use python and module psycopg2 for access to our database, this way provide tools for automated inserting our data from excel file to tables in database, also it is safe;</p>

Step 1 create new database:

```sql
psql
CREATE DATABASE lab_1
```

Step 2 connect to database:

```python
connection = psycopg2.connect(database='lab_1', user='alex', password='')
cursor = connection.cursor()
```
After success connection, we may use cursor object for interact with database.

Step 3 create tables:

```python
cursor.execute("CREATE TABLE Areas("+
               "short_n VARCHAR(10) PRIMARY KEY NOT NULL,"+
               "full_n VARCHAR(255) NOT NULL)")
```

Step 4 insert data to table:

```python
areas = pd.read_csv('areas.csv')
for short_n, full_n in areas.values:
    cursor.execute("INSERT INTO Areas (short_n, full_n) "+
    "VALUES (%s, %s )", (short_n, full_n))
```
Read data like pandas DataFrame object, this object has many useful and powerfull properties, but we just use it for iteration in for loop. 

```python
  short_n       full_n
0       K        Kelly
1       P      Parsons
2       B  Bound River
3       T    Tirrawara
4       S  Southerland
5       A        Alice
6       D       Darwin
```

Step 5 after some tests, we may commit  changes in database:

```python
connection.commit()
```
As result we have database:
![alt text](https://github.com/yougooo/db_course/blob/master/LAB_1/lab_1.png)

UPDATE 

If just import from source excel file without preprocesing, we catch some errors. Data have duplication, in table 'measurments' we have columns 'point_z' and 'area',  this columns describe location, but not measurment. That's why better drop 'area' column from 'measurments' table (we have same column in 'stations' table, and if  for example it is stantion '1' it is 100% 'B' area). And take data from point_z and put it into new column 'point_z' in table 'stations'. New database relations look like this:  
![alt text](https://github.com/yougooo/db_course/blob/master/LAB_1/lab_1_2.png)
