# Zoom Lecture 12
# use ipython instead of jupyter notebook
# pull up webcam 
# make sure we're repointing very often (faster than 4 min ?)

import ugradio
ugradio.interf??
# limits of the alt az of the interferometer
ugradio.interf.ALT_MIN
ugradio.interf.ALT_MAX
ugradio.interf.AZ_MIN
ugradio.interf.AZ_MAX

# create interferometer object
interf = ugradio.itnterf.Interferometer()
interf.get_pointing() # where interf is currently pointing
interf.point(45, 225) # random orientaiton
interf.point(45, 45) # will generate error: az is out of bounds
interf.point(135, 225) # instead, flip it over the top instead of around the side
interf.stow() # always finsih every observation with this

# pointing: use astropy to do coordinates
import astropy.coordinates
import astropy.time
import time
time.time()
t = astropy.time.Time(time.time(), format='unix')
sun = astropy.coordinates.get_sun(t)
# OR: ugradio.coord.sunpos and ugradio.coord.moonpos
sun.ra
sun.dec
type(sun.ra) # astrpy.coorindates.angles.Longitude
sun.ra.deg # converts to degrees
sun.ra.rad # converts to radians
# convert to Earth coordinates
ugradio.nch # use this to get current lat long and alt
obs = astropy.coordinates.EarthLocation(lon=ugradio.nch.lon, lat=ugradio.nch.lat, height=ugradio.nch.alt)

# we now have all the info to compute where the sun is relative to us
# we have the time and the location of the earth and the location of the sun 
altaz = astropy.coordinates.AltAz(obstime=t, location=obs) # defines a time and a location on earth
pointing = sun.transform_to(altaz)
# sun coordinates: sun's alt and az
pointing.alt
pointing.az
interf.point(pointing.alt.deg, pointing.az.deg) # could set wait=False to do other stuff while the telescope is moving
interf.get_pointing() # currently where the interfs are pointing
interf.wait() # see if the interfs are done pointing

# SUMMARY:
import ugradio
import astropy.coordinates
import astropy.time
import time

interf = ugradio.interf.Interferometer()

t = astropy.time.Time(time.time(), format='unix')
sun = astropy.coordinates.get_sun(t)
obs = astropy.coordinates.EarthLocation(lon=ugradio.nch.lon, lat=ugradio.nch.at, height=ugradio.nch.alt)

for i in range(10): # get 10 observations
    print('Pointing')
    t = astropy.time.Time(time.time(), format='unix')
    altaz = astropy.coordinates.AltAz(obstime=t, location=obs)
    pointing = sun.transform_to(altaz)
    interf.point(pointing.alt.deg, pointing.az.deg, wait=False)
    interf.get_pointing()
    time.sleep(10)








# Zoom Lecture 13
import matplotlib.pylab as plt
import numpy as np

import ugradio
ugradio.hp_multi??

# measure the current voltage value
hpm.read_voltage()

# be careful about using time.sleep - this won't create equally spaced time intervals
import time
data, times = [], []
for i in range(10):
    t0 = time.time()
    v = hpm.read_voltage()
    data.append(v)
    times.append(t0)
    time.sleep(1-(time.time()-t0))

plt.plot(times, data)
plt.show()

np.diff(times)

# don't use time.sleep, use built in hpm methods:
hpm.get_recording_data??
hpm.start_recording(1) # will run in the background!
hpm.get_recording_status()
volts,times = hpm.get_recording_data() # will still run in the background!
# if ^ looks good, can end the recording, otherwise can continue running
np.savez('backup.npz', volts=volts, times=times)
hpm.end_recording()
np.savez('final_sun.npz', volts=volts, times=times)

# if stuff quits and fails:
# use a try and except loop so that you don't exit the program
# catch pointing error, etc.
# save the data and stop the recording
try:
    print(data[0])
except(IndexError):
    print('index error')

# note: figure out what happens when the sun sets!