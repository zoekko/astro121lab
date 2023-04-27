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

sleep_time = 39600 #s, sleep for this duration of time before beginning to track
TEST_ON_MOON = False # track moon as a test 

def galactic_to_altaz(coord, time):
    '''convert galactic coords to altaz coords'''
    l, b = coord
    g_sc = SkyCoord(frame="galactic", l=l*u.deg, b=b*u.deg)
    altaz_sc = g_sc.transform_to(AltAz(obstime=time, location=LOC))
    return altaz_sc.alt.degree, altaz_sc.az.degree

save_dir = '/home/radiolab/Desktop/bpi/astro121lab/lab4/data/'
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

# set the LO such that HI shows up at 150 MHz
LO = 635 #MHz
synclient = ugradio.agilent.SynthClient()
synclient.set_frequency(LO, unit='MHz')
logging.info(f'LO set to: {LO} MHz')

LOC = EarthLocation(lat=37.91934*u.deg, lon=122.15385*u.deg, height=304*u.m)
ALT_MIN, ALT_MAX = leusch.ALT_MIN, leusch.ALT_MAX
AZ_MIN, AZ_MAX = leusch.AZ_MIN, leusch.AZ_MAX

pointings = np.load('/home/radiolab/Desktop/bpi/astro121lab/lab4/pointings.npy')

# first pointing: do calibration 
noisediode = ugradio.leusch.LeuschNoise()
noisediode.on()
logging.info('Turned on noise diode')
gal_coord = pointings[0]
l, b = gal_coord
alt, az = galactic_to_altaz(gal_coord, Time(datetime.now()))
logging.info(f'alt az set to: {alt}, {az}')

if TEST_ON_MOON:
    # get the coordinates of the moon to test
    t = astropy.time.Time(time.time(), format='unix')
    moon = ugradio.coord.moonpos(jd=t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
    alt, az = ugradio.coord.get_altaz(moon[0], moon[1], t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)

# read data
fname = f'{save_dir}CALIBRATION{t}_{l}_{b}'
N = 10 # try dif values of N and explore how this affects SNR
spec = ugradio.leusch.Spectrometer()
num_times_failed = 0 # the number of times the telescope failed to point 
fail_threshold = 5 # if pointing fails more than this number of times, quit
successful_pointing=True
while successful_pointing:
    try:
        telescope.point(alt, az)
        logging.info(f'CALIBRATION: telescope now pointing at: {telescope.get_pointing()}')
        spec.read_spec(fname, N, (l,b), 'ga')
        successful_pointing=False
    except(AssertionError):
        logging.info(f'CALIBRATION: Unsuccessful pointing, trying again in a second')
        num_times_failed+= 1
        if num_times_failed > fail_threshold:
            logging.info(f'CALIBRATION: More than {fail_threshold} failed tries: break')
            successful_pointing=False
        time.sleep(1)
noisediode.off()
logging.info('Turned off noise diode')

failed_coords = [] # save the coordinates that are out of bounds and go back to them later
for gal_coord in pointings:
    l, b = gal_coord
    alt, az = galactic_to_altaz(gal_coord, Time(datetime.now()))

    if TEST_ON_MOON:
        # get the coordinates of the moon to test
        t = astropy.time.Time(time.time(), format='unix')
        moon = ugradio.coord.moonpos(jd=t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)
        alt, az = ugradio.coord.get_altaz(moon[0], moon[1], t, lat=ugradio.nch.lat, lon=ugradio.nch.lon, alt=ugradio.nch.alt)

    # read data
    t = Time(time.time(), format='unix').value
    logging.info(f'Time (unix time): {t}')
    logging.info(f'alt az set to: {alt}, {az}')
    
    fname = f'{save_dir}{t}_{l}_{b}.fits'
    spec = ugradio.leusch.Spectrometer()

    num_times_failed = 0 # the number of times the telescope failed to point 
    successful_pointing=True
    while successful_pointing:
        try:
            telescope.point(alt, az)
            logging.info(f'telescope now pointing at: {telescope.get_pointing()}')
            spec.read_spec(fname, N, (l,b), 'ga')
            successful_pointing=False
        except(AssertionError):
            logging.info(f'Unsuccessful pointing, trying again in a second')
            num_times_failed+= 1
            if num_times_failed > fail_threshold:
                logging.info(f'More than ten failed tries: break and add to queue')
                failed_coords += [list(gal_coord)]
                successful_pointing=False
            time.sleep(1)
            
            
# # run on previously failed coordinates
# logging.info(f'Running on previously failed coordinates.')
# for gal_coord in failed_coords:
#     l, b = gal_coord
#     alt, az = galactic_to_altaz(gal_coord, Time(datetime.now()))

#     # read data
#     t = Time(time.time(), format='unix').value
#     logging.info(f'Time (unix time): {t}')
#     logging.info(f'Previously failed coordinate (l, b): {l}, {b}')
#     logging.info(f'alt az set to: {alt}, {az}')
    
#     fname = f'{save_dir}take2_{t}_{l}_{b}.fits'
#     spec = ugradio.leusch.Spectrometer()

#     successful_pointing=True
#     while successful_pointing:
#         try:
#             telescope.point(alt, az)
#             logging.info(f'telescope now pointing at: {telescope.get_pointing()}')
#             spec.read_spec(fname, N, (l,b), 'ga')
#             successful_pointing=False
#         except(AssertionError):
#             logging.info(f'Unsuccessful pointing, trying again in a minute')
#             time.sleep(60)
            

# george's edit:
# run on previously failed coordinates
logging.info(f'Running on previously failed coordinates.')
complete = False
while complete==False:
    gal_coord = list(failed_coords).pop(0)
    l, b = gal_coord
    alt, az = galactic_to_altaz(gal_coord, Time(datetime.now()))

    # read data
    t = Time(time.time(), format='unix').value
    logging.info(f'Time (unix time): {t}')
    logging.info(f'Previously failed coordinate (l, b): {l}, {b}')
    logging.info(f'alt az set to: {alt}, {az}')
    
    fname = f'{save_dir}take2_{t}_{l}_{b}.fits'
    spec = ugradio.leusch.Spectrometer()
    try:
        telescope.point(alt, az)
        logging.info(f'telescope now pointing at: {telescope.get_pointing()}')
        spec.read_spec(fname, N, (l,b), 'ga')
    except(AssertionError):
        logging.info(f'Unsuccessful pointing, moving onto next failed coordinate in a minute')
        failed_coords += [list(gal_coord)]
        time.sleep(60)
    if len(failed_coords) == 0:
        complete = True
            
            
telescope.stow()