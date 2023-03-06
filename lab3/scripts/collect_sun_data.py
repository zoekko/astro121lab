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
import snap_spec

save_dir = '/home/pi/Desktop/sun'
total_time = 60 # duration of observation in minutes

# create interferometer object
interf = ugradio.interf.Interferometer()
spec = snap_spec.snap.UGRadioSnap()
spec.initialize(mode='corr')

t0 = astropy.time.Time(time.time(), format='unix')
t_e = 0
print('start time (JD): ')
print(t0)
all_data = np.array([])
i = 0

while t_e < total_time:
    print('')
    print('iteration: ')
    print(i)
    # get the coordinates of the sun in RA and DEC
    t = astropy.time.Time(time.time(), format='unix')
    print('time elapsed (min): ')
    t_e = t - t0
    t_e = t_e * 24 * 60
    print(t_e)
    sun = astropy.coordinates.get_sun(t)
    # convert coordinates to alt az (Earth coordinates)
    obs = astropy.coordinates.EarthLocation(lon=ugradio.nch.lon, lat=ugradio.nch.lat, height=ugradio.nch.alt)
    altaz = astropy.coordinates.AltAz(obstime=t, location=obs) # defines a time and a location on earth
    pointing = sun.transform_to(altaz)
    print('sun is currently at: ')
    print('alt: ')
    print(pointing.alt.deg)
    print('az: ')
    print(pointing.az.deg)
    
    # 3/6/23 EDIT: point interf twice
    interf.point(pointing.alt.deg, pointing.az.deg) # could set wait=False to do other stuff while the telescope is moving
    interf.point(pointing.alt.deg, pointing.az.deg)
    print('interf now pointing at: ')
    print(interf.get_pointing()) # currently where the interfs are pointing
    # interf.wait() # see if the interfs are done pointing
    
    # collect data
    try:
        data = spec.read_data()
        all_data = np.append(all_data, data)
        np.save(save_dir, all_data)
    except(AssertionError):
        print('Assertion Error: trying again')
        data = spec.read_data()
        all_data = np.append(all_data, data)
        np.save(save_dir, all_data)
        
    i += 1
    
print('')
print('Finished collecting data!')
interf.stow() # always finsih every observation with this
interf.stow()
print('interf stowed at: ')
print(interf.get_pointing())
