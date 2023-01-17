# collect data from the signal generator

import ugradio
import numpy as np
import matplotlib.pylab as plt

anti_aliasing_filter = False # use the SDR default anti-aliasing filter
mixing = True # use the SDR mixer (SSB)
center_freq = 26*1000*1000

save_dir = '/home/radiopi/Desktop/' # directory to save data into
take = '_6'

# signal frequency
sig_freq = 0*1000

# sampling frequency
samp_freq = 3200*1000

# create SDR object
if mixing:
    if anti_aliasing_filter:
        print('mixing with default anti-aliasing filter')
        our_sdr = ugradio.sdr.SDR(direct=False, center_freq=center_freq, sample_rate=samp_freq, gain=2)
    elif not anti_aliasing_filter: # over-ride the default anti-aliasing filter
        print('mixing with NO default anti-aliasing filter')
        our_sdr = ugradio.sdr.SDR(direct=False, center_freq=center_freq, sample_rate=samp_freq, fir_coeffs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2047]), gain='auto')
elif not mixing:
    if anti_aliasing_filter:
        print('NO mixing with default anti-aliasing filter')
        our_sdr = ugradio.sdr.SDR(sample_rate=samp_freq)
    elif not anti_aliasing_filter: # over-ride the default anti-aliasing filter
        print('NO mixing with default anti-aliasing filter')
        our_sdr = ugradio.sdr.SDR(sample_rate=samp_freq, fir_coeffs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2047]))
our_data = our_sdr.capture_data(nsamples=2048, nblocks=1)


    
np.save(save_dir+'ssb_digital_'+str(int(samp_freq/1000))+ take, our_data)