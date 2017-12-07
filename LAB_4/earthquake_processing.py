
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import re
import psycopg2


# In[2]:

earth_data = pd.read_csv('Mag6PlusEarthquakes_1900-2013.csv', parse_dates=True)


# In[3]:

earth_data.describe()


# ![title](lab_4.png)

# In[110]:

connection = psycopg2.connect(database='lab_4', user='alex', password='')
cursor = connection.cursor()


# In[111]:

cursor.execute("DROP TABLE IF EXISTS earthquake")
cursor.execute("DROP TABLE IF EXISTS locations")
cursor.execute("DROP TABLE IF EXISTS places")
cursor.execute("DROP TABLE IF EXISTS net")
cursor.execute("DROP TABLE IF EXISTS magnitude")
cursor.execute("DROP TABLE IF EXISTS stations")


# In[112]:

event_list = list(map(lambda i: (earth_data['place'][i]), xrange(len(earth_data['longitude']))))
print len(event_list)
print len(set(event_list))


# In[108]:

#cursor.execute("CREATE EXTENSION postgis")


# In[113]:

cursor.execute("CREATE TABLE net("+
               "net_id SERIAL UNIQUE,"+
               "net varchar(15) PRIMARY KEY)")


# In[114]:

cursor.execute("CREATE TABLE places("
               "place_id SERIAL PRIMARY KEY,"+
               "place varchar(255))")


# ### Earthquake may happen in same points, of course not so frequently, but its not good for database table. Column 'place' have 755 unique values. May be improved by creating event table. Now primary key is 'local_id', bad choise but it is give posipility to quick import data to database for some tests.

# In[115]:

cursor.execute("CREATE TABLE locations("+
               "local_id SERIAL UNIQUE,"+
               "coord geometry(Point, 4326),"
               "depth real,"+
               "place int4 REFERENCES places(place_id),"+
               "net int4 REFERENCES net(net_id),"+
               "PRIMARY KEY(local_id))")


# In[116]:

cursor.execute("CREATE TABLE magnitude("+
               "mag_id SERIAL UNIQUE,"+
               "magtype varchar(5) PRIMARY KEY)")


# In[117]:

cursor.execute("CREATE TABLE stations("+
               "station_id SERIAL PRIMARY KEY,"+
               "nst int4,"+
               "gap real,"+
               "dmin real,"+
               "rms real)")


# In[118]:

cursor.execute("CREATE TABLE earthquake("+
               "id varchar(255) PRIMARY KEY,"+
               "time timestamp NOT NULL,"+
               "location int4 REFERENCES locations(local_id),"+
               "mag float NOT NULL,"+
               "magnitude int4 REFERENCES magnitude(mag_id),"+
               "receive_station int4 REFERENCES stations(station_id),"+
               "update_time timestamp NOT NULL)"
                )


# In[119]:

mag_list = list(set(earth_data['magType']))
print mag_list


# In[120]:

# insert data into magnitude table
for mag in mag_list:
    cursor.execute("INSERT INTO magnitude (magtype) VALUES (%s)", (mag,))


# In[121]:

net_list = list(set(earth_data['net']))
print net_list


# In[122]:

# insert data into net table
for net in net_list:
    cursor.execute("INSERT INTO net (net) VALUES (%s)", (net,))


# ### For insert data with key, python have great dictionary realization. And it is way to do complex key in database.

# In[123]:

dict_maker = lambda data_list: {key:item for key,item in zip(data_list, range(1,len(data_list)+1))}


# In[124]:

place_list = list(set(earth_data['place']))


# In[125]:

for place in place_list:
    cursor.execute("INSERT INTO places (place) VALUES (%s)", (place,))


# In[126]:

net_dict = dict_maker(net_list)
mag_dict = dict_maker(mag_list)
place_dict = dict_maker(place_list)


# In[127]:

for i in range(len(earth_data['longitude'])):
    coord = 'POINT( {} {} )'.format(earth_data['longitude'][i],earth_data['latitude'][i])
    cursor.execute("INSERT INTO locations (coord, depth, place, net) VALUES (ST_PointFromText( %s,4326 ), %s, %s, %s)",
                  (coord, earth_data['depth'][i], place_dict[earth_data['place'][i]], net_dict[earth_data['net'][i]],))


# In[128]:

earth_data['nst'] = earth_data['nst'].replace(np.nan, 0)
earth_data['gap'] = earth_data['gap'].replace(np.nan, 0)
earth_data['dmin'] = earth_data['dmin'].replace(np.nan, 0)
earth_data['rms'] = earth_data['rms'].replace(np.nan, 0)


# In[129]:

for i in range(len(earth_data['longitude'])):
        cursor.execute("INSERT INTO stations (nst, gap, dmin, rms) VALUES (%s, %s, %s, %s)",
                       (earth_data['nst'][i],earth_data['gap'][i],earth_data['dmin'][i],earth_data['rms'][i]),)


# In[130]:

for i in range(len(earth_data['longitude'])):
    cursor.execute("INSERT INTO earthquake (id, time, location, mag, magnitude, receive_station, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (earth_data['id'][i],earth_data['time'][i],place_dict[earth_data['place'][i]],
                        earth_data['mag'][i], mag_dict[earth_data['magType'][i]], i+1, earth_data['updated'][i]))


# In[131]:

connection.commit()
cursor.close()
connection.close()


# In[ ]:



