import psycopg2
import pandas as pd
import numpy as np


#
# Create table and relation
#

connection = psycopg2.connect(database='lab_1', user='alex', password='')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Measurments")
cursor.execute("DROP TABLE IF EXISTS Stations")
cursor.execute("DROP TABLE IF EXISTS Areas")


cursor.execute("CREATE TABLE Areas("+
               "short_n VARCHAR(10) NOT NULL PRIMARY KEY,"+
               "full_n VARCHAR(255) NOT NULL)")


cursor.execute("CREATE TABLE Stations ("+
               "Area VARCHAR(10) NOT NULL REFERENCES Areas(short_n),"+
               "Station int4 NOT NULL,"+
               "station_id SERIAL PRIMARY KEY,"+
               "POINT_X REAL NOT NULL,"+
               "POINT_Y REAL NOT NULL,"+
               "UNIQUE(Area, Station))")                                

cursor.execute("CREATE TABLE Measurments ("+
               "id SERIAL,"+
               "Date DATE NOT NULL,"+
               "Time TIME NOT NULL,"+
               "base_station int4 REFERENCES Stations (station_id),"+
               "POINT_Z REAL,"+
               "P1 REAL,"+
               "P2 SMALLINT,"+
               "P3 SMALLINT,"+
               "P4 REAL,"+
               "PRIMARY KEY(Date, Time, base_station))")

#
# Insert data into table
#

areas = pd.read_csv('areas.csv')
for short_n, full_n in areas.values:
    cursor.execute("INSERT INTO Areas (short_n, full_n) "+
                   "VALUES (%s, %s )", (short_n, full_n))


stations = pd.ExcelFile("DB_Lab1_Data.xls").parse('Stations')
for area, station, point_x, point_y in stations.values:
    cursor.execute("INSERT INTO Stations (Area, Station, POINT_X, POINT_Y)"+
                   " VALUES (%s, %s, %s, %s) ", (area, station, point_x, point_y))

"""
measurments = pd.read_csv('Measurments.csv')
for date, time, area, station, point_z, p1,p2,p3,p4 in measurments.values:
    #print date, time, area, station, point_z, p1,p2,p3,p4
    cursor.execute("INSERT INTO Measurments (Date,Time,Station,Area,POINT_Z,P1,P2,P3,P4)"+
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ", (date,time, station,area,point_z,p1,p2,p3,p4))
"""
### move point_z form measurments to stations ###

cursor.execute("ALTER TABLE stations ADD COLUMN point_z real NOT NULL DEFAULT 'NaN'")
#cursor.execute("SELECT station, point_z FROM measurments WHERE point_z != 'NaN' ORDER BY station")
"""
temp_point_z = [] 

for row in cursor:
    temp_point_z.append(row)

for num,val in temp_point_z:
    print val
    cursor.execute("UPDATE stations SET point_z = (%s) WHERE station=(%s)", (val, num))
    
"""
cursor.execute("ALTER TABLE measurments DROP COLUMN point_z")
#cursor.execute("ALTER TABLE measurments DROP COLUMN station")

#############################################

connection.commit()

#
# Selection from database 
#
"""
##### Task 1 #####
cursor.execute("SELECT * FROM Measurments WHERE Date > '2001-01-01' and Date < '2003-01-01';")
print "Task 1"
for row in cursor:
    print row


##### Task 2 #####
cursor.execute("SELECT stations.*, areas.full_n FROM stations JOIN areas ON stations.area=areas.short_n ORDER BY full_n;")
print "Task 2"
for row in cursor:
    print row


##### Task 3 #####
cursor.execute("SELECT * FROM measurments WHERE Time < '12:00'")
print "Task 3"
for row in cursor:
    print row


##### Task 4 #####

cursor.execute("SELECT measurments.*, areas.full_n FROM measurments JOIN stations ON measurments.station=stations.station"+
               " JOIN areas ON stations.area=areas.short_n "+
               "WHERE full_n = 'Alice' or full_n = 'Darwin'")
print "Task 4"
for row in cursor:
    print row

##### Task 5 #####
cursor.execute("SELECT 2*P1+100*P2+cos(P4) AS P5 FROM measurments")
print "Task 5"
for row in cursor:
    print row
"""
cursor.close()
connection.close()


