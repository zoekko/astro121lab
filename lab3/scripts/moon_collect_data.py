# collect data from the moon for ~ 10 hours
# use ipython instead of jupyter notebook
# pull up webcam 
# make sure we're repointing very often (faster than 4 min ?)

import ugradio
import ugradio.coord
import astropy.coordinates
import astropy.time
import time
import matplotlib.pylab as plt
import numpy as np
import snap_spec

save_dir = '/home/pi/Blueberry Pi/astro121lab/lab3/data/moon/full_night_moon'
total_time = 10*60 # duration of observation in minutes

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
    # get the coordinates of the moon in RA and DEC
    t = astropy.time.Time(time.time(), format='unix')
    moon = ugradio.coord.moonpos(jd=t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
    pointing = ugradio.coord.get_altaz(moon[0], moon[1], t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)

    # pointing
    print('moon is currently at: ')
    print('alt: ')
    print(pointing[0])
    print('az: ')
    print(pointing[1])

    # 3/6/23 EDIT: point interf twice
    interf.point(pointing[0], pointing[1]) # could set wait=False to do other stuff while the telescope is moving
    interf.point(pointing[0], pointing[1])
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
