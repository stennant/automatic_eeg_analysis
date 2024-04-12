import matplotlib.pyplot as plt


def plot_all_data(data):
    plt.figure(1)
    plt.plot(data.iloc[:,0], data.iloc[:,1], linewidth=1.0)
    plt.xlabel('Time(sec)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.title('Time History')
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_trace_eg.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()

def plot_data_with_seizures_marked(data, seizure_start_times, seizure_end_times):
    plt.figure(1)
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], linewidth=1.0)
    plt.xlabel('Time(sec)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.title('Time History')
    try:
        for rowcount, row in enumerate(seizure_start_times):
            plt.hlines(y=200, xmin=seizure_start_times[rowcount], xmax=seizure_end_times[rowcount], linestyle='-',
                       color='red', linewidth=2)
    except TypeError:
        plt.hlines(y=200, xmin=seizure_start_times[0], xmax=seizure_end_times[0], linestyle='-', color='red',
                   linewidth=2)
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_markedtrace_eg.png',
                dpi=200)
    plt.draw()
    plt.show()
    plt.close()


def plot_continuous_data(t, amp):
    plt.figure(1)
    plt.plot(t, amp, linewidth=1.0)
    plt.xlabel('Time(sec)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.title('Time History')
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_trace.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()


def plot_fft(ff, zz):
    plt.figure(2)
    plt.plot(ff,zz)
    plt.grid(True)
    plt.title(' FFT Magnitude ')
    plt.ylabel(' Amplitude ')
    plt.xlabel(' Frequency (Hz) ')
    plt.grid(True, which="both")
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_fft.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()

def plot_fft_phase(ff, ph, pi):
    plt.figure(3)
    plt.plot(ff,ph*(180./pi))
    plt.grid(True)
    plt.title(' FFT Phase ')
    plt.ylabel(' Phase (deg) ')
    plt.xlabel(' Frequency (Hz) ')
    plt.grid(True, which="both")
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_fft-phase.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()


def plot_fft_log(ff, b, NHS):
    plt.figure(4)
    plt.plot(ff,b[0:int(NHS)])
    plt.grid(True)
    plt.title(' log(abs(fft(a)) ')
    plt.ylabel(' Magnitude ')
    plt.xlabel(' Frequency (Hz) ')
    plt.grid(True, which="both")
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_log-of-fft.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()

def plot_cepstrum(t, c, NHS):
    plt.figure(5)
    plt.plot(t[1:int(NHS)],(c[1:int(NHS)].real))
    plt.title('Cepstrum  ifft(log(abs(fft(a))))')
    plt.ylabel('Amplitude')
    plt.xlabel('Quefrency(sec)')
    plt.grid(True)
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()

    plt.figure(6)
    plt.plot(1/(t[1:int(NHS)]),(c[1:int(NHS)].real))
    plt.xlim(0,100)
    plt.title('Cepstrum  ifft(log(abs(fft(a))))')
    plt.ylabel('Amplitude')
    plt.xlabel('1/Quefrency(sec)')
    plt.grid(True)
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum_hz.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()


def plot_cepstrum_theta_range(theta_band_data):
    plt.figure(7)
    plt.plot(theta_band_data[:,0], theta_band_data[:,1])
    plt.title('Cepstrum  ifft(log(abs(fft(a))))')
    plt.ylabel('Amplitude')
    plt.xlabel('Quefrency(sec)')
    plt.grid(True)
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum-theta.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()


def plot_normalised_cepstrum(theta_band_data, normalized_vector):
    plt.figure(8)
    plt.plot(theta_band_data[:,0], normalized_vector)
    plt.title('Cepstrum  ifft(log(abs(fft(a))))')
    plt.ylabel('Amplitude normalised to max')
    plt.xlabel('Quefrency(sec)')
    plt.grid(True)
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum-theta_normalisedtomax.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()


def plot_zscore_cepstrum(theta_band_data, theta_amplitude_zscore):
    plt.figure(9)
    plt.plot(theta_band_data[:,0], theta_amplitude_zscore)
    plt.title('Cepstrum  ifft(log(abs(fft(a))))')
    plt.ylabel('z-score')
    plt.xlabel('Quefrency(sec)')
    plt.axhline(2.2, linestyle='--',color='black', linewidth=2)
    plt.axhline(0.2, linestyle='--',color='black', linewidth=2)
    plt.axhline(0.02, linestyle='--',color='black', linewidth=2)
    plt.grid(True)
    plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum-theta_zscore.png', dpi=200)
    plt.draw()
    plt.show()
    plt.close()
