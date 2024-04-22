from __future__ import print_function

from math import log,atan2,pi
import math
from numpy import floor,zeros,mean
from numpy import argmax
import numpy as np
import pandas as pd
from scipy import stats
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import cepstrum_plots
import time

class FFT:

    def __init__(self,a,b,dt):
        self.a=a
        self.b=b
        self.dt=dt

    def fft_data(self):

#   Truncate to 2**n

        num=len(self.b)

        noct=int(log(num)/log(2))

        num_fft=2**noct

        bb=self.b[0:num_fft]

        dur_fft=num_fft*self.dt

        df=1/dur_fft

        z =fft(bb)

        nhalf=num_fft/2

        #print (" ")
        #print (" %d samples used for FFT " %num_fft)
        #print ("df = %8.4g Hz" %df)

        zz=zeros(int(nhalf),'f')

        ph=zeros(int(nhalf),'f')

        freq=zeros(num_fft,'f')

        z/=float(num_fft)

        for k in range(0,int(num_fft)):
            freq[k]=k*df

        ff=freq[0:int(nhalf)]

        for k in range(0,int(nhalf)):

            if(k > 0):
                zz[k]=2.*abs(z[k])
            else:
                zz[k]= abs(z[k])

            ph[k]=atan2(z.real[k],z.imag[k])

        idx = argmax(abs(zz))

        return idx,freq,ff,z,zz,ph,nhalf,df,num_fft


def round_down(num, divisor):
    return num - (num % divisor)


def window_data(data):
    times = np.arange(0, 1, 1/250)
    amplitude = np.asarray(data["main_eeg_channel"])
    num = int(amplitude.shape[0]) #N = sampling_rate * duration

    return times, amplitude, num


def cepstrum_calculation(num, amplitude, dt, times):

    # cepstrum_plots.plot_continuous_data(times, amplitude) # plot the raw signal to check

    amplitude = amplitude.tolist()

    N=int(2**floor(log(num)/log(2.)))

    if(N<num):  # zeropad
        N=2*N
        for i in range(num,int(N)):
            amplitude.append(0.)

    NHS=N/2

    idx,freq,ff,z,zz,ph,nhalf,df,num_fft=FFT(times,amplitude,dt).fft_data()

    # plot the fft results
    #cepstrum_plots.plot_fft(ff, zz)

    a=z.real + z.imag*1j

    nnn=len(a)

    b=zeros(nnn,'f')

    for i in range(0,int(nnn)):
        try:
            b[i]=log(abs(a[i]))
        except ValueError:
            b[i] = np.nan

    # plot log of FFT
    #cepstrum_plots.plot_fft_log(ff, b, NHS)

    c=ifft(b)

    # plot cepstrum results in quefrency and Hz
    #cepstrum_plots.plot_cepstrum(t, c, NHS)

    return c, times, NHS


def normalize_vector_max(vector):
    max_abs = np.max(np.abs(vector))
    if max_abs == 0:
        return vector
    return vector / max_abs


def identify_theta_peaks(c, t, NHS):

    upper_theta_range = 0.1 #1/10 # divide by 1 to get quefrency
    lower_theta_range = 0.2 #1/5 # divide by 1 to get quefrency

    cepstrum_data = np.vstack((t[1:int(NHS)], c[1:int(NHS)].real)) # quefrency, amplitude
    cepstrum_data = np.transpose(cepstrum_data)

    # extract data in the theta frequency range
    upper_theta_band_data = cepstrum_data[cepstrum_data[:,0] >= upper_theta_range]
    theta_band_data = upper_theta_band_data[upper_theta_band_data[:,0] <= lower_theta_range]

    normalized_vector = normalize_vector_max(theta_band_data[:,1])
    theta_amplitude_zscore = stats.zscore(normalized_vector)

    # plot quefrency in the theta range (0.1 to 0.2)
    #cepstrum_plots.plot_cepstrum_theta_range(theta_band_data)

    # plot quefrency normalised by max value
    #cepstrum_plots.plot_normalised_cepstrum(theta_band_data, normalized_vector)

    # plot z scored quefrency
    #cepstrum_plots.plot_zscore_cepstrum(theta_band_data, theta_amplitude_zscore)

    threshold = 2.2
    marker = 0

    quefrency_above_threshold = np.where(theta_amplitude_zscore[:] >= threshold)[0]
    if len(quefrency_above_threshold) > 0:
        marker = 1

    return marker


def control_cepstrum_anaylsis(data):

    #cepstrum_plots.plot_all_data(data) # if you want to plot the whole continuous data
    print('Running cepstral analysis ....')
    start = time.process_time() # so I can measure the time it takes for code to run

    # we want to analyse the data in 1 second windows that slide i.e. move by 0.2 seconds
    window_duration = 250 # how long in samples we want to analyse (1 second = 250 samples)
    slide_duration = 50 # how much to move the window for each analysis in samples (50 samples is 0.2 seconds)
    total_duration = round_down(data.shape[0], 250) # round down duration in samples to the nearest second

    total_windows = int((total_duration - window_duration) / slide_duration + 1)

    cepstrum_score = np.zeros(shape=(int(total_duration), total_windows))

    for i in range(total_windows):

        if i == 0: # this is so it doesn't start at 50 samples
            rowstart = i
            rowend = rowstart + window_duration
        else:
            rowstart = i * slide_duration
            rowend = rowstart + window_duration

        # Extract data to run on cepstrum analysis
        times,amplitude,num = window_data(data.iloc[rowstart:rowend, :])

        # Basic stats of continuous data
        sr = 250
        dt = 1/sr
        start = time.process_time()  # so I can measure the time it takes for code to run

        # run cepstral analysis on windowed data
        c, t, NHS = cepstrum_calculation(num, amplitude, dt, times)

        #ceptrum_time = time.process_time() - start
        #print('cepstrum code took ' + str(ceptrum_time) + ' to run')
        #start = time.process_time()  # so I can measure the time it takes for code to run

        # identify if there are peaks in theta in quefrency data - returns 1 if there is, 0 if not
        marker = identify_theta_peaks(c, t, NHS)
        #end_time = time.process_time() - start
        #print('theta peaks took ' + str(end_time) + ' to run')

        marker_array = np.repeat(marker, window_duration)
        cepstrum_score[rowstart:rowend, i] = marker_array

    return cepstrum_score, data, total_duration