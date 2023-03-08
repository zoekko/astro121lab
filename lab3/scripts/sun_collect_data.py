# point at sun and collect data using threading

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
import threading

def track():
    i=0
    t0 = astropy.time.Time(time.time(), format='unix')
    t_e = 0
    print('Tracking start time (JD): ')
    print(t0)
    while t_e < total_time:
        print('')
        print('Iteration: ')
        print(i)
        # get the coordinates of the sun in RA and DEC
        t = astropy.time.Time(time.time(), format='unix')
        print('Tracking time elapsed (min): ')
        t_e = t - t0
        t_e = t_e * 24 * 60
        print(t_e)
        sun = astropy.coordinates.get_sun(t)
        # convert coordinates to alt az (Earth coordinates)
        altaz = astropy.coordinates.AltAz(obstime=t, location=obs) # defines a time and a location on earth
        pointing = sun.transform_to(altaz)
        print('Sun is currently at: ')
        print('alt: ')
        print(pointing.alt.deg)
        print('az: ')
        print(pointing.az.deg)

        # 3/6/23 EDIT: point interf twice: not necessary 
        try:
            interf.point(pointing.alt.deg, pointing.az.deg) # could set wait=False to do other stuff while the telescope is moving
            interf.point(pointing.alt.deg, pointing.az.deg)
            print('interf now pointing at: ')
            print(interf.get_pointing()) # currently where the interfs are pointing
        except(AssertionError):
            print('Assertion Error: trying again')
            interf.point(pointing.alt.deg, pointing.az.deg)
        i += 1
        
def record():
    all_data = np.array([])
    prev_cnt = None
    t0 = astropy.time.Time(time.time(), format='unix')
    t_e = 0
    print('Recording start time (JD): ')
    print(t0)
    while t_e < total_time:
        t = astropy.time.Time(time.time(), format='unix')
        print('Recording time elapsed (min): ')
        t_e = t - t0
        t_e = t_e * 24 * 60
        print(t_e)
        # collect data
        data = spec.read_data(prev_cnt=prev_cnt)
        prev_cnt = data['acc_cnt']
        all_data = np.append(all_data, data)
        np.save(save_dir, all_data)
    
if __name__=="__main__":
    
    save_dir = '/home/pi/Blueberry Pi/astro121lab/lab3/data/sun/full_day_sun_pt2'
    total_time = 8*60 # duration of observation in minutes

    # create interferometer object
    interf = ugradio.interf.Interferometer()
    spec = snap_spec.snap.UGRadioSnap()
    spec.initialize(mode='corr')
    obs = astropy.coordinates.EarthLocation(lon=ugradio.nch.lon, lat=ugradio.nch.lat, height=ugradio.nch.alt)

    thrd = threading.Thread(target=track)
    thrd.start()
    time.sleep(15) # give interfs time to point to sun
    record()
    print('')
    print('Finished collecting data!')
    interf.stow() # always finsih every observation with this
    interf.stow()
    print('interf stowed at: ')
    print(interf.get_pointing())
