import ugradio
from ugradio import leusch

import astropy.coordinates
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
import astropy.time
from astropy.time import Time
import astropy.units as u

from datetime import datetime
import time

import matplotlib.pylab as plt
import numpy as np
import logging

save_dir = '/home/radiolab/Desktop/bpi/astro121lab/data/'
logging.basicConfig(filename=f'{save_dir}orion.log', level=logging.INFO)
# get coordinates of where we want to point
t = Time(time.time(), format='unix').value
logging.info(f'First tracking start time (JD): {t}')

# create LeuschTelescope object
telescope = ugradio.leusch.LeuschTelescope()

# set the LO such that HI is in the center of the bandpass


LOC = EarthLocation(lat=37.91934*u.deg, lon=122.15385*u.deg, height=304*u.m)
ALT_MIN, ALT_MAX = leusch.ALT_MIN, leusch.ALT_MAX
AZ_MIN, AZ_MAX = leusch.AZ_MIN, leusch.AZ_MAX

def galactic_to_altaz(coord, time):
    l, b = coord
    g_sc = SkyCoord(frame="galactic", l=l*u.deg, b=b*u.deg)
    altaz_sc = g_sc.transform_to(AltAz(obstime=time, location=LOC))
    return altaz_sc.alt.degree, altaz_sc.az.degree

pointings = np.load('/home/zoeko/astro121lab/lab4/pointings.npy')
for gal_coord in pointings:
    alt, az = galactic_to_altaz(gal_coord, Time(datetime.now()))
    l, b = gal_coord
    
    # read data
    t = Time(time.time(), format='unix').value
    fname = f'{save_dir}/{t}_{alt}_{az}'
    N = 10 # try dif values of N and explore how this affects SNR
    spec = ugradio.leusch.Spectrometer()

    num_times_failed = 0 # the number of times the telescope failed to point 
    fail_threshold = 10 # if pointing fails more than this number of times, quit

    successful_pointing=True
    while successful_pointing:
        try:
            telescope.point(alt, az)
            logging.info(f'telescope now pointing at: {telescope.get_pointing()}')
            spec.read_spec(fname, N, (l,b), 'ga')
        except(AssertionError):
            logging.info(f'Unsuccessful pointing, trying again in a minute')
            num_times_failed+= 1
            if num_times_failed > fail_threshold:
                logging.info(f'More than ten failed tries: break')
                successful_pointing==False
            time.sleep(60)

            
           
    
    