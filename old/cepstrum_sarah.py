import parameters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

prm = parameters.Parameters()

def plot_raw_signal(main_eeg_channel):
    time = np.asarray(main_eeg_channel["time"])
    amplitude = np.asarray(main_eeg_channel["5"])

    plt.figure(1)
    plt.plot(time, amplitude, linewidth=1.0)
    plt.xlabel('Time(sec)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.title('Time History')
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_trace_own.png', dpi=200)
    plt.draw()


    return time, amplitude

def fft_data(time, amplitude, sampling_rate):

    # Number of samples in normalized_tone
    N = int(amplitude.shape[0]) #N = sampling_rate * duration

    yf = fft(amplitude)
    xf = fftfreq(N, 1 / sampling_rate)

    plt.plot(xf, np.abs(yf))
    plt.show()

    return yf, xf


def run_cepstrum_analysis(main_eeg_channel ):
    sampling_rate = 250
    time, amplitude = plot_raw_signal(main_eeg_channel)

    yf, xf = fft_data(time, amplitude, sampling_rate)

    return

