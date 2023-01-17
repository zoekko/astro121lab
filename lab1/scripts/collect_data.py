# collect data from the signal generator

import ugradio
import numpy as np
import matplotlib.pylab as plt

anti_aliasing_filter = True # use the SDR default anti-aliasing filter

save_dir = '/home/radiopi/Desktop/' # directory to save data into

take = ''

# signal frequency
sig_freq = 700 * 1000

# sampling frequency
samp_freq = 2400*1000

# create SDR object
if anti_aliasing_filter:
    our_sdr = ugradio.sdr.SDR(sample_rate=samp_freq)
elif not anti_aliasing_filter: # over-ride the default anti-aliasing filter
     our_sdr = ugradio.sdr.SDR(sample_rate=samp_freq, fir_coeffs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2047]))
our_data = our_sdr.capture_data()
    
np.save(save_dir+'two_freq_10_'+str(int(samp_freq/1000))+'_'+ take, our_data)