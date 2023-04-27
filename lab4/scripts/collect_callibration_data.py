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

sleep_time = 9000 #s, sleep for this duration of time before beginning to track
pointings = np.load('/home/radiolab/Desktop/bpi/astro121lab/lab4/pointings.npy')

# # where to point for callibration 
# gal_coord = np.array([160., -70.])

def galactic_to_altaz(coord, time):
    '''convert galactic coords to altaz coords'''
    l, b = coord
    g_sc = SkyCoord(frame="galactic", l=l*u.deg, b=b*u.deg)
    altaz_sc = g_sc.transform_to(AltAz(obstime=time, location=LOC))
    return altaz_sc.alt.degree, altaz_sc.az.degree

save_dir = '/home/radiolab/Desktop/bpi/astro121lab/lab4/cal_data/'
logging.basicConfig(filename=f'{save_dir}orion.log', level=logging.INFO)

# go to sleep 
t = Time(time.time(), format='unix').value
logging.info(f'Current unix time: {t}')
logging.info(f'Going to sleep for {sleep_time} seconds.')
time.sleep(sleep_time)
t = Time(time.time(), format='unix').value
logging.info(f'Current unix time: {t}')

# create LeuschTelescope object
telescope = ugradio.leusch.LeuschTelescope()
noisediode = ugradio.leusch.LeuschNoise()
spec = ugradio.leusch.Spectrometer()

# set the LO such that HI shows up at 150 MHz
LO = 635 #MHz
synclient = ugradio.agilent.SynthClient()
synclient.set_frequency(LO, unit='MHz')
logging.info(f'LO set to: {LO} MHz')

LOC = EarthLocation(lat=37.91934*u.deg, lon=122.15385*u.deg, height=304*u.m)
ALT_MIN, ALT_MAX = leusch.ALT_MIN, leusch.ALT_MAX
AZ_MIN, AZ_MAX = leusch.AZ_MIN, leusch.AZ_MAX


for gal_coord in pointings:
    # turn on noise diode and calculate where to point

    l, b = gal_coord
    alt, az = galactic_to_altaz(gal_coord, Time(datetime.now()))
    logging.info(f'alt az set to: {alt}, {az}')

    t = Time(time.time(), format='unix').value
    # point + read data
    on_fname = f'{save_dir}ON_{l}_{b}_{t}'
    off_fname = f'{save_dir}OFF_{l}_{b}_{t}'
    N = 10 # try dif values of N and explore how this affects SNR
    
    try:
        noisediode.on()
        logging.info('Turned on noise diode')
        telescope.point(alt, az)
        logging.info(f'CALIBRATION: telescope now pointing at: {telescope.get_pointing()}')
        spec.read_spec(on_fname, N, (l,b), 'ga')
        noisediode.off()
        logging.info('Turned off noise diode')
        spec.read_spec(off_fname, N, (l,b), 'ga')
    except(AssertionError):
        logging.info(f'CALIBRATION: Unsuccessful pointing, moving on to next point')
    noisediode.off()
    logging.info('Turned off noise diode')
            
            
telescope.stow()