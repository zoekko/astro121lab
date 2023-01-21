# turn off anti-aliasing filter

import ugradio
import numpy as np
import matplotlib.pylab as plt

# sampling frequency
freq = 1000*1000

# create SDR object
our_sdr = ugradio.sdr.SDR(sample_rate=freq, fir_coeffs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2047]))
our_data = our_sdr.capture_data()
    
np.save('nofilter_freq'+str(int(freq/1000)), our_data)