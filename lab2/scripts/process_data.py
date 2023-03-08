import numpy as np
import os

in_path = '../data'
out_path = '../out'
fileList = ['on', 'off', 'cold', 'cal']

def fft(data, num_samp=2048, samp_rate=3.2e6):
    f = np.fft.fftshift(np.fft.fftfreq(num_samp, 1/samp_rate))
    Fx = np.fft.fftshift(np.fft.fft(data))
    return f, Fx

def average_power(data):
    f, Fx = fft(data)
    pwr = np.abs(Fx)**2
    avg_pwr = np.mean(pwr, axis=0)
    return f, avg_pwr

# pre-process data

raw_data = {}
pwr_data = {}
target_freq_res = 2e3 # Hz

try:
    os.mkdir(out_path)
except OSError as error:
    print(error) 

for fins in fileList:
    in_fname = f'{in_path}/s_' + fins + '_3200.npy'
    out_fname = f'{out_path}/p_' + fins + '_3200.npz'
    data = np.load(in_fname)
    raw_data[fins] = data
    f, avg_pwr = average_power(data)
    # f, avg_pwr = adjust_freq_res(f, avg_pwr, target_freq_res)
    # avg_pwr = interference(avg_pwr)
    
    pwr_data[fins] = [f, avg_pwr]
    np.savez(out_fname, f=f, p=avg_pwr)
        