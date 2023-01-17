# collect data from the generator

import ugradio
import numpy as np
import matplotlib.pylab as plt

anti_aliasing_filter = True # use the default anti-aliasing filter

save_dir = '/home/radiopi/Desktop/' # directory to save data into

# signal frequency
sig_freq = 1000 * 1000

# sampling frequency
samp_freq = 1000*1000

# create SDR object
if anti_aliasing_filter:
    our_sdr = ugradio.sdr.SDR(sample_rate=freq)
elif not anti_aliasing_filter: # over-ride the default anti-aliasing filter
     our_sdr = ugradio.sdr.SDR(sample_rate=freq, fir_coeffs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2047]))
our_data = our_sdr.capture_data()
    
np.save('nofilter_freq'+str(int(freq/1000)), our_data)