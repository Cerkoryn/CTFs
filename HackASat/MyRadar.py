from skyfield.elementslib import OsculatingElements
from skyfield.positionlib import Geocentric
from skyfield.timelib import Timescale
from skyfield.api import load
from poliastro.bodies import Earth
from poliastro.iod import izzo
from astropy import units as u
from math import *
import numpy
import skyfield
import datetime

# THIS IS AN INCOMPLETE SOLUTION
# WE NEEDED TO USE LAMBERT'S EQUATIONS
# TO SOLVE FOR VELOCITY INSTEAD OF
# JUST DISTANCE TRAVELLED OVER TIME

earthGM = 3.986004418e5       # Km/s**2.

# For t1
t1 = datetime.datetime(2021, 6, 27, 0, 9, 51, tzinfo=datetime.timezone.utc)
azimuthDeg = 231.7485858
elevationDeg = 12.54592798
slantRange = 5327.313337*1000

# For t2
t2 = datetime.datetime(2021, 6, 27, 0, 9, 52, tzinfo=datetime.timezone.utc)
azimuthDeg2 = 231.7440785
elevationDeg2 = 12.62728479
slantRange2 = 5325.195435*1000

obs_lat = 8.7256        # Degrees
obs_long = 167.715      # Degrees
obs_alt = 35            # Meters
obs_x = -6160.446*1000       # Meters
obs_y = 1341.509*1000        # Meters
obs_z = 961.181*1000         # Meters

def aer2ecef(azimuthDeg, elevationDeg, slantRange, obs_lat, obs_long, obs_alt):
    xyz = []

    #site ecef in meters
    sitex = obs_x
    sitey = obs_y
    sitez = obs_z

    #some needed calculations
    slat = sin(radians(obs_lat))
    slon = sin(radians(obs_long))
    clat = cos(radians(obs_lat))
    clon = cos(radians(obs_long))

    azRad = radians(azimuthDeg)
    elRad = radians(elevationDeg)

    # az,el,range to sez convertion
    south  = -slantRange * cos(elRad) * cos(azRad)
    east   =  slantRange * cos(elRad) * sin(azRad)
    zenith =  slantRange * sin(elRad)


    xyz.append((( slat * clon * south) + (-slon * east) + (clat * clon * zenith) + sitex)/1000)
    xyz.append(((slat * slon * south) + ( clon * east) + (clat * slon * zenith) + sitey)/1000)
    xyz.append(((-clat *        south) + ( slat * zenith) + sitez)/1000)

    return xyz

posVec1 = aer2ecef(azimuthDeg, elevationDeg, slantRange, obs_lat, obs_long, obs_alt)*u.km
posVec2 = aer2ecef(azimuthDeg2, elevationDeg2, slantRange2, obs_lat, obs_long, obs_alt)*u.km

distTravelledVec = []
for i in range(0, 3):
    distTravelledVec.append(posVec2[i]-posVec1[i])

print(f"Position Vector at t1: {posVec1}")
print(f"Position Vector at t2: {posVec2}")
#print(f"Distance travelled at t2: {distTravelledVec}")
velVec = izzo.lambert(Earth.k, posVec1, posVec2, u.min*60)
for i in velVec:
    (velVec1, velVec2) = i
    #print(i)
    velVec3 = []
    for item in velVec1.value:
        velVec3.append(float(item))
    posVec3 = []
    for item in posVec2.value:
        posVec3.append(float(item))

    print(posVec3)
    print(velVec3)

    # Setting up an object with Keplerian elements from ICRF
    ts = load.timescale()
    time = Timescale.utc(ts, 2021, 6, 27, 0, 9, 52)
    pos2 = skyfield.units.Distance(km=posVec3)
    vel2 = skyfield.units.Velocity(km_per_s=velVec3)
    g = Geocentric(pos2.au, vel2.au_per_d, time, center=399)
    kepler = OsculatingElements(g.position, g.velocity, time, earthGM)

    print(kepler.semi_major_axis.km)
    print(kepler.eccentricity)
    print(kepler.inclination.degrees)
    print(kepler.longitude_of_ascending_node.degrees)
    print(kepler.argument_of_periapsis.degrees)
    print(kepler.true_anomaly.degrees)
