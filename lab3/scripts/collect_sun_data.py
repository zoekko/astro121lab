# collect data from the sun for ~ 1 hour
# use ipython instead of jupyter notebook
# pull up webcam 
# make sure we're repointing very often (faster than 4 min ?)

import ugradio
import astropy.coordinates
import astropy.time
import time
import matplotlib.pylab as plt
import numpy as np

# create interferometer object
interf = ugradio.itnterf.Interferometer()


for i in range(10): # get 10 observations
    # where interf is currently pointing
    print('interf currently pointing at: ')
    interf.get_pointing() 

    # get the coordinates of the sun in RA and DEC
    t = astropy.time.Time(time.time(), format='unix')
    sun = astropy.coordinates.get_sun(t)
    # convert coordinates to alt az (Earth coordinates)
    obs = astropy.coordinates.EarthLocation(lon=ugradio.nch.lon, lat=ugradio.nch.lat, height=ugradio.nch.alt)
    altaz = astropy.coordinates.AltAz(obstime=t, location=obs) # defines a time and a location on earth
    pointing = sun.transform_to(altaz)
    print('sun is currently at: ')
    print('alt: ')
    pointing.alt
    print('az: ')
    pointing.az
    
    interf.point(pointing.alt.deg, pointing.az.deg) # could set wait=False to do other stuff while the telescope is moving
    print('interf now pointing at: ')
    interf.get_pointing() # currently where the interfs are pointing
    # interf.wait() # see if the interfs are done pointing
    
    # collect data 
    




# Zoom Lecture 13
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


interf.stow() # always finsih every observation with this
