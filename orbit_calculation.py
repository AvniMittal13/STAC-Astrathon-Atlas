# pip install sgp4
from astropy.constants import G, M_earth
import numpy as np
from pytz import timezone
from datetime import timedelta
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
import scipy
from pprint import pprint
from sgp4 import exporter
import sys
from numpy import add
from sgp4.api import Satrec
import pandas as pd
import json

from sgp4.functions import days2mdhms

sat_name = sys.argv[1]
l1 = sys.argv[2]
l2 = sys.argv[3]
que_lat = sys.argv[4]
que_lon = sys.argv[5]
day = sys.argv[6]
month = sys.argv[7]
year = sys.argv[8]

# print(que_lat,que_lon)

satellite = Satrec.twoline2rv(l1, l2)


fields = exporter.export_omm(satellite, sat_name)
print(fields)    # printing satellite info obtained from TLE  ====1====

Orbit_Period = (24*3600)/fields['MEAN_MOTION']

u = G*M_earth
a = ((((Orbit_Period)**2)*u)/(4*(scipy.pi)**2))**(1/3)

# pip install skyfield


ts = load.timescale()
satellite_f = EarthSatellite(l1, l2, sat_name, ts)
# print(satellite_f)

# print(satellite_f.epoch.utc_jpl())

# PART 2 --- finding longitude, latitude and altitude
t = ts.now()
geocentric = satellite_f.at(t)
# print(geocentric.position.km)


lat, lon = wgs84.latlon_of(geocentric)
# print('Latitude:', lat)
# print('Longitude:', lon)
altitude = wgs84.height_of(geocentric)
# print('Altitude: ',altitude.km)

q2_data = {"Latitude": str(lat), "Longitude": str(
    lon), "Altitude": str(altitude.km)}
print(json.dumps(q2_data))   # ======== 2 =======
# json.loads(q2_data)

# PART 3 --- given longitude and latitude, find when next visible
bluffton = wgs84.latlon(float(que_lat), float(que_lon))


eastern = timezone('US/Eastern')

start_time = ts.now()
t_inc = start_time
y_n = 0


range = np.arange(0, Orbit_Period, 20)
t_arr = ts.utc(float(year), float(month), float(day), 0, 0, range)

# e = eastern.localize(timedelta(hours=20/3600))
# add = ts.from_datetime(e)

for i in t_arr:
    # t_inc = t_inc + add*i
    difference = satellite_f - bluffton
    topocentric = difference.at(i)
    # geocentric = satellite_f.at(t_inc)
    alt, az, distance = topocentric.altaz()
    if(alt.degrees > 30 or alt.degrees < 150):
        y_n = 1
        break

if(y_n == 1):
    date_visible = str(i.utc.year) + '/' + \
        str(i.utc.month) + '/' + str(i.utc.day)
    ans3 = "Yes, satellite will be visible on "+date_visible+". Move " + \
        str(distance) + " "+str(az.degrees) + "degrees clockwise from North"
else:
    ans3 = "Satellite is not visible from the given location"

q3_data = {"ans": ans3}
print(json.dumps(q3_data))   # ======== 3 =======


# PART 4

t_check = ts.utc(float(year), float(month), float(day))
difference = satellite_f - bluffton
topocentric = difference.at(t_check)
# geocentric = satellite_f.at(t_inc)
alt, az, distance = topocentric.altaz()
if(alt.degrees > 30 or alt.degrees < 150):
    ans = "Satellite is visible, Move " + \
        str(distance) + " "+str(az.degrees) + "degrees clockwise from North"

else:
    ans = "Satellite is not visible"

q4_data = {"ans": ans}
print(json.dumps(q4_data))   # ======== 4 =======
# print(Orbit_Period)
# sys.stdout.flush()
