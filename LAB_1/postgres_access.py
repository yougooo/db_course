import psycopg2
import pandas as pd

#
# Create table and relation
#

connection = psycopg2.connect(database='lab_1', user='alex', password='95qaz26plm')

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Measurments")
cursor.execute("DROP TABLE IF EXISTS Stations")
cursor.execute("DROP TABLE IF EXISTS Areas")


#cursor.execute("DROP TABLE IF EXISTS Areas")
cursor.execute("CREATE TABLE Areas("+
               "short_n VARCHAR(10) PRIMARY KEY NOT NULL,"+
               "full_n VARCHAR(255) NOT NULL)")


#cursor.execute("DROP TABLE IF EXISTS Stations")
cursor.execute("CREATE TABLE Stations ("+
               "Area VARCHAR(10) NOT NULL REFERENCES Areas (short_n),"+
               "Stations SMALLINT PRIMARY KEY NOT NULL,"+
               "POINT_X REAL NOT NULL,"+
               "POINT_Y REAL NOT NULL)")                                


#cursor.execute("DROP TABLE IF EXISTS Measurments")
cursor.execute("CREATE TABLE Measurments ("+
               "id SERIAL PRIMARY KEY,"+
               "Date DATE NOT NULL,"+
               "Time TIME NOT NULL,"+
               "Area VARCHAR(10) NOT NULL REFERENCES Areas (short_n),"+
               "Station SMALLINT NOT NULL REFERENCES Stations (Stations),"+
               "POINT_Z REAL,"+
               "P1 REAL NOT NULL,"+
               "P2 SMALLINT NOT NULL,"+
               "P3 SMALLINT NOT NULL,"+
               "P4 REAL NOT NULL)")

#
# Insert data into table
#

areas = pd.read_csv('DB_Lab1_Data.csv')
for short_n, full_n in areas.values:
    cursor.execute("INSERT INTO Areas (short_n, full_n) "+
                   "VALUES (%s, %s )", (short_n, full_n))


stations = pd.ExcelFile("DB_Lab1_Data.xls").parse('Stations')
for area, station, point_x, point_y in stations.values:
    cursor.execute("INSERT INTO Stations (Area, Stations, POINT_X, POINT_Y)"+
                   " VALUES (%s, %s, %s, %s) ", (area, station, point_x, point_y))


measurments = pd.read_csv('Measurments.csv')
for date, time, area, station, point_z, p1,p2,p3,p4 in measurments.values:
    #print date, time, area, station, point_z, p1,p2,p3,p4
    cursor.execute("INSERT INTO Measurments (Date,Time,Area,Station,POINT_Z,P1,P2,P3,P4)"+
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ", (date,time,area,station,point_z,p1,p2,p3,p4))

connection.commit()

#
# Selection from database 
#

##### Task 1 #####
cursor.execute("SELECT * FROM Measurments WHERE Date > '2001-01-01' and Date < '2003-01-01';")
print "Task 1"
for row in cursor:
    print row
##### Task 2 #####
cursor.execute("SELECT stations, point_x, point_y FROM stations ORDER BY area;")
print "Task 2"
for row in cursor:
    print row

##### Task 3 #####
cursor.execute("SELECT * FROM measurments WHERE Time < '12:00'")
print "Task 3"
for row in cursor:
    print row


##### Task 4 #####
cursor.execute("SELECT * FROM measurments WHERE Area = 'A' or Area = 'D'")print "Task 4"
for row in cursor:
    print row

##### Task 5 #####
cursor.execute("SELECT 2*P1+100*P2+cos(P4) AS P5 FROM measurments")
print "Task 5"
for row in cursor:
    print row


cursor.close()
connection.close()


