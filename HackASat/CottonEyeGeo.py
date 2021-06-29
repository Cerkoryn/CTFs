from orbital.utilities import mean_anomaly_from_true
from pwn import *
from skyfield.timelib import Time, Timescale
from skyfield.positionlib import ICRF, Geocentric
from skyfield.elementslib import *
import skyfield
import datetime
import numpy
from skyfield.api import load, EarthSatellite, wgs84
from orbital import earth, KeplerianElements, Maneuver, plot
from scipy.constants import kilo
import matplotlib.pyplot as plt


#This gets you all of your original orbit, except with the Mean Anomaly shifted to when the satelite is at Apogee (180 degrees or pi radians from perigee)
molniya3 = KeplerianElements(a=24732.96738133805*kilo, e=0.7068077979296534, i=math.radians(0.11790360842507447), raan=math.radians(90.22650379956278), arg_pe=math.radians(226.58754885495142), M0=mean_anomaly_from_true(0.7068077979296534, math.radians(180)), body=earth)
plot(molniya3, title='Cotton Eye Geo')
print(f"Velocity vector before burn: [{molniya3.v[0]/1000}, {molniya3.v[1]/1000}, {molniya3.v[2]/1000}]")

#This is your new orbit that you will have after the manuever
molniya2 = KeplerianElements(a=42164*kilo, e=0, i=math.radians(0), raan=math.radians(0), arg_pe=math.radians(0), M0=mean_anomaly_from_true(0.7068077979296534, math.radians(180)), body=earth)
plot(molniya2, title='Cotton Eye Geo')
print(f"New velocity vector: [{molniya2.v[0]/1000}, {molniya2.v[1]/1000}, {molniya2.v[2]/1000}]")

# Uncomment this to plot both orbits if you want.
#plt.show()

#Subtract the velocity vector from the first orbit from the second orbit's velocity vector.
x=((molniya2.v[0]/1000)-(molniya3.v[0]/1000))-2.1053   # Fudged a little bit
y=((molniya2.v[1]/1000)-(molniya3.v[1]/1000))+0.8384   # Fudged a little bit
z=((molniya2.v[2]/1000)-(molniya3.v[2]/1000))

print(f"Delta-v of x: {x}")
print(f"Delta-v of y: {y}")
print(f"Delta-v of z: {z}\n")

# Setting up an object with Keplerian elements
ts = load.timescale()
time = Timescale.utc(ts, 2021, 6, 26, 19, range(20,1460))
pos = numpy.array([8449.401305, 9125.794363, -17.461357])
vel = numpy.array([-1.419072, 6.780149, 0.002865])
pos2 = skyfield.units.Distance(km=pos)
vel2 = skyfield.units.Velocity(km_per_s=vel)
g = Geocentric(pos2.au, vel2.au_per_d, time, 399)
kepler = OsculatingElements(g.position, g.velocity, Timescale.utc(ts, 2021, 6, 26, 19, 20), 3.986004418e5)

# This is to calculate the period from perigee, then find the apogee one-half period after that.
# Apogee is when you want to do your burn.
print(f"Periapsis time: {kepler.periapsis_time.utc_datetime()}")
print(f"Period in days: {kepler.period_in_days}") 
burnTime = kepler.periapsis_time.utc_datetime()+datetime.timedelta(days=(0.44803240376126185/2))
print(f"Apoapsis time: {burnTime}\n")

def run():
    io = remote('visual-sun.satellitesabove.me', 5014)
    time = f'2021-06-27-00:13:45.166-UTC'  # Fudged a little bit
    print(f'\nSending: {time}')
    print(f'Sending: {x}')
    print(f'Sending: {y}')
    print(f'Sending: {z}\n')
    io.sendafter('Ticket please:\n', 'ticket{sierra347984whiskey2:GCgrrwDVh3EEgyJV014cInJjwQrQvUHHXEkGNQygy92Z3HSjNpUpld0ZMzttwQmN_g}\n', timeout=3)
    io.recv()
    io.sendline(time)
    io.recv()
    io.sendline(str(x))
    io.recv()
    io.sendline(str(y))
    io.recv()
    io.sendline(str(z))
    io.recvuntil('New Orbit (a, e, i, Ω, ω, υ, t):')
    result = io.recv()
    pprint(result)
    results = [result.split()[i] for i in range(6)]

    a = float(results[0].decode('UTF-8')) #semi major axis
    e = float(results[1].decode('UTF-8')) #eccentricity
    i = float(results[2].decode('UTF-8')) #inclination
    o = float(results[3].decode('UTF-8')) #longitude of the center node
    w = float(results[4].decode('UTF-8')) #argument of perapsis
    u = float(results[5].decode('UTF-8')) #true anomaly

    #radius from true anomaly
    altitude = a * ((1 - (e*e)) / (1 + (e * math.cos(math.radians(u)))))
    io.close()
    
    print(f'Time: {time}, Altitude: {altitude}')

run()
