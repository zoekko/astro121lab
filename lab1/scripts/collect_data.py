import ugradio
import numpy as np
import matplotlib.pylab as plt

# sampling frequency
freq = 2200*1000

# create SDR object
our_sdr = ugradio.sdr.SDR(sample_rate=freq)
our_data = our_sdr.capture_data()
    
np.save('freq'+str(int(freq/1000)), our_data)