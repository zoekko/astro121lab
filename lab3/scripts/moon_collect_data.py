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
import logging

def track():
    i=0
    t0 = astropy.time.Time(time.time(), format='unix')
    t_e = 0
    logging.info(f'Tracking start time (JD): {t0}')
    while t_e < total_time:
        logging.info('')
        logging.info(f'Iteration: {i}')
        # get the coordinates of the moon in RA and DEC
        t = astropy.time.Time(time.time(), format='unix')
        t_e = t - t0
        t_e = t_e * 24 * 60
        logging.info(f'Tracking time elapsed (min): {t_e}')
        moon = ugradio.coord.moonpos(jd=t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
        pointing = ugradio.coord.get_altaz(moon[0], moon[1], t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
        logging.info(f'Moon is currently at alt, az: {pointing[0]}, {pointing[1]}')

        # 3/6/23 EDIT: point interf twice: not necessary 
        try:
            interf.point(pointing[0], pointing[1]) # could set wait=False to do other stuff while the telescope is moving
            interf.point(pointing[0], pointing[1])
            logging.info(f'interf now pointing at: {interf.get_pointing()}')
        except(AssertionError):
            logging.warning('Assertion Error in pointing: trying again')
        i+=1
        
def record():
    i=0
    prev_cnt = None
    t0 = astropy.time.Time(time.time(), format='unix')
    t_e = 0
    logging.info(f'Recording start time (JD): {t0}')
    while t_e < total_time:
#     while True:
        t = astropy.time.Time(time.time(), format='unix')
        t_e = t - t0
        t_e = t_e * 24 * 60
        logging.info(f'Recording time elapsed (min): {t_e}')
        # collect data
        try:
            data = spec.read_data(prev_cnt=prev_cnt)
            prev_cnt = data['acc_cnt']
            np.save(f'{save_dir}moon_{i}', data)
            i+=1
        except(AssertionError):
            logging.warning('Assertion Error in recording: trying again')
            prev_cnt = None
    
           
    
if __name__=="__main__":
    
    save_dir = '/home/pi/Blueberry Pi/astro121lab/lab3/data/moon/full_night_moon/'
    logging.basicConfig(filename=f'{save_dir}full_night_moon_log.log', level=logging.INFO)
    total_time = 9*60 # duration of observation in minutes

    # create interferometer object
    interf = ugradio.interf.Interferometer()
    spec = snap_spec.snap.UGRadioSnap()
    spec.initialize(mode='corr')
    obs = astropy.coordinates.EarthLocation(lon=ugradio.nch.lon, lat=ugradio.nch.lat, height=ugradio.nch.alt)
   
    # point to moon - first check bounds on observation
    risen = False
    while risen == False:
        t = astropy.time.Time(time.time(), format='unix')
        logging.info(f'First tracking start time (JD): {t}')
        moon = ugradio.coord.moonpos(jd=t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
        pointing = ugradio.coord.get_altaz(moon[0], moon[1], t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
        logging.info(f'Moon is currently at alt, az: {pointing[0]}, {pointing[1]}')
        if not (pointing[0] > ugradio.interf.ALT_MIN and
            pointing[0] < ugradio.interf.ALT_MAX and
            pointing[1] > ugradio.interf.AZ_MIN and
            pointing[1] < ugradio.interf.AZ_MAX):
            logging.info(f'Moon has not risen yet')
            time.sleep(60)
            continue
        else:
            risen == True
    interf.point(pointing[0], pointing[1])
    
    # start threading
    thrd = threading.Thread(target=track)
    thrd.start()
    record()
    logging.info('Finished collecting data!')
    interf.stow() # always finsih every observation with this
    interf.stow()
    logging.info(f'interf stowed at: {interf.get_pointing()}')