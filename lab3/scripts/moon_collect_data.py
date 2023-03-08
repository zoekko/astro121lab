# point at moon and collect data using threading

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
        
        moon = ugradio.coord.moonpos(jd=t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
        pointing = ugradio.coord.get_altaz(moon[0], moon[1], t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)

        # pointing
        print('moon is currently at: ')
        print('alt: ')
        print(pointing[0])
        print('az: ')
        print(pointing[1])


        # 3/6/23 EDIT: point interf twice: not necessary 
        try:
            interf.point(pointing[0], pointing[1])
            interf.point(pointing[0], pointing[1])
            print('interf now pointing at: ')
            print(interf.get_pointing())
        except(AssertionError):
            print('Assertion Error: trying again')
            interf.point(pointing[0], pointing[1])
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
    
    save_dir = '/home/pi/Blueberry Pi/astro121lab/lab3/data/sun/full_night_moon'
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