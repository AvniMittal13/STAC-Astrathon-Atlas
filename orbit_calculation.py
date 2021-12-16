# pip install sgp4
import sys
from sgp4.api import Satrec
import pandas as pd
import json

from sgp4.functions import days2mdhms

sat_name = sys.argv[1]
l1 = sys.argv[2]
l2=sys.argv[3]
que_lat=sys.argv[4]
que_lon=sys.argv[5]
day=sys.argv[6]
month=sys.argv[7]
year=sys.argv[8]

# print(que_lat,que_lon)

satellite = Satrec.twoline2rv(l1, l2)

from sgp4 import exporter
from pprint import pprint

fields = exporter.export_omm(satellite, sat_name)
print(fields)    # printing satellite info obtained from TLE  ====1====

Orbit_Period = (24*3600)/fields['MEAN_MOTION']

from astropy.constants import G,M_earth
import scipy
u = G*M_earth
a= ((((Orbit_Period)**2)*u)/(4*(scipy.pi)**2))**(1/3)

# pip install skyfield

from skyfield.api import EarthSatellite
from skyfield.api import load, wgs84

ts = load.timescale()
satellite_f = EarthSatellite(l1, l2, sat_name, ts)
# print(satellite_f)

# print(satellite_f.epoch.utc_jpl())

# PART 2 --- finding longitude, latitude and altitude
t=ts.now()
geocentric = satellite_f.at(t)
# print(geocentric.position.km)


lat, lon = wgs84.latlon_of(geocentric)
# print('Latitude:', lat)
# print('Longitude:', lon)
altitude = wgs84.height_of(geocentric)
# print('Altitude: ',altitude.km)

q2_data = {"Latitude": str(lat), "Longitude": str(lon), "Altitude": str(altitude.km) }
# df_q2=pd.DataFrame(q2_data)
# q2_res = df_q2.to_json(orient="table")
print(json.dumps(q2_data))   # ======== 2 =======
# json.loads(q2_data)

# PART 3 --- given longitude and latitude, find when next visible
# bluffton = wgs84.latlon(float(que_lat), float(que_lon))
# t_check = ts.utc(float(year), float(month), float(day))


# sys.stdout.flush()