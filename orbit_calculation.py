# pip install sgp4
import sys
from sgp4.api import Satrec

sat_name = sys.argv[1]
l1 = sys.argv[2]
l2=sys.argv[3]

satellite = Satrec.twoline2rv(l1, l2)

from sgp4 import exporter
from pprint import pprint

fields = exporter.export_omm(satellite, sat_name)
pprint(fields)

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
print(satellite_f)

print(satellite_f.epoch.utc_jpl())

# PART 2 --- finding longitude, latitude and altitude
t=ts.now()
geocentric = satellite_f.at(t)
print(geocentric.position.km)
lat, lon = wgs84.latlon_of(geocentric)
print('Latitude:', lat)
print('Longitude:', lon)
altitude = wgs84.height_of(geocentric)
print('Altitude: ',altitude.km)

# PART 3 --- given longitude and latitude, find when next visible
bluffton = wgs84.latlon(+40.8939, -83.8917)
t0 = ts.utc(2014, 1, 23)
t1 = ts.utc(2014, 1, 24)

# sys.stdout.flush()