###########################################################################
# program: cepstrum.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: September 12, 2013
# description:
#    This script calculates the cepstrum of a time history signal.
#
#    The time history must have two columns: time(sec) & amplitude
#
#############################################################################

from __future__ import print_function


from tompy_functions import read_two_columns_from_dialog
from tompy_functions import signal_stats,sample_rate_check
from tompy_functions import GetInteger2

from math import log,atan2,pi

from numpy import floor,zeros,mean
from numpy import argmax
import numpy as np
from scipy import stats

from scipy.fftpack import fft,ifft

import matplotlib.pyplot as plt

#############################################################################

class FFT:

    def __init__(self,a,b,imr,dt):
        self.a=a
        self.b=b
        self.imr=imr
        self.dt=dt


    def fft_data(self):

#   Truncate to 2**n

        num=len(self.b)

        noct=int(log(num)/log(2))

        num_fft=2**noct

        bb=self.b[0:num_fft]

        if(self.imr==1):
            bb=bb-mean(bb)

        dur_fft=num_fft*self.dt

        df=1/dur_fft


        z =fft(bb)

        nhalf=num_fft/2

        print (" ")
        print (" %d samples used for FFT " %num_fft)
        print ("df = %8.4g Hz" %df)

        zz=zeros(int(nhalf),'f')
        #ff=zeros(nhalf,'f')
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

#############################################################################

class READ_DATA:

    def __init__(self):
        pass

    @classmethod
    def check_data(cls,a,b,num,sr,dt):

        sample_rate_check(a,b,num,sr,dt)

        return sr,dt

    def read_and_stats(self):

        label="Enter the acceleration time history..."

        a,b,num =read_two_columns_from_dialog(label)

        sr,dt,ave,sd,rms,skew,kurtosis,dur=signal_stats(a,b,num)

        sr,dt=READ_DATA.check_data(a,b,num,sr,dt)

        return a,b,num,sr,dt,dur

#############################################################################

print (" ")

t,amp,n,sr,dt,dur=READ_DATA().read_and_stats()

plt.figure(1)
plt.plot(t, amp, linewidth=1.0)
plt.xlabel('Time(sec)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.title('Time History')
plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_trace.png', dpi=200)
plt.draw()
plt.show()

N=int(2**floor(log(n)/log(2.)))

print (" time history length = %d " %n)

if(N<n):  # zeropad
    N=2*N
    for i in range(n,int(N)):
        amp.append(0.)

NHS=N/2

print (" ")
print (" Remove mean:  1=yes  2=no ")

imr = GetInteger2()

idx,freq,ff,z,zz,ph,nhalf,df,num_fft=FFT(t,amp,imr,dt).fft_data()

print (" ")
print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(ff[idx],zz[idx]))


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

#############################################################################

a=z.real + z.imag*1j

nnn=len(a)

b=zeros(nnn,'f')

for i in range(0,int(nnn)):
    b[i]=log(abs(a[i]))

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

#############################################################################

c=ifft(b)

plt.figure(5)

plt.plot(t[1:int(NHS)],(c[1:int(NHS)].real))
plt.title('Cepstrum  ifft(log(abs(fft(a))))')
plt.ylabel('Amplitude')
plt.xlabel('Quefrency(sec)')
#plt.axvline(8.5, color='limegreen', linewidth=100, alpha=0.4, zorder=0)
plt.grid(True)
plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum.png', dpi=200)
plt.draw()
plt.show()

#############################################################################
print('Saving cepstrum data ....')
amplitude = t[1:int(NHS)]
quefrency = c[1:int(NHS)].real

amplitude_zscore = stats.zscore(amplitude[1:])
#quefrency_zscore = stats.zscore(quefrency)


plt.figure(6)

plt.plot(amplitude_zscore,quefrency[1:])
plt.title('Cepstrum  ifft(log(abs(fft(a))))')
plt.ylabel('z-score')
plt.xlabel('Quefrency(sec)')
#plt.axvline(8.5, color='limegreen', linewidth=100, alpha=0.4, zorder=0)
plt.grid(True)
plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum-zscore.png', dpi=200)
plt.draw()
plt.show()

#############################################################################

cepstrum_data = np.vstack((amplitude, quefrency))
cepstrum_data = np.reshape(cepstrum_data,  (cepstrum_data.shape[1], 2))

lower_theta_range = 5
upper_theta_range = 10

upper_quefrency_theta = 1/5
lower_quefrency_theta = 1/10

# extract data in the theta frequency range
upper_theta_band_data = cepstrum_data[cepstrum_data[:,1] >= lower_quefrency_theta]
theta_band_data = upper_theta_band_data[upper_theta_band_data[:,1] <= upper_quefrency_theta]

def normalize_vector_max(vector):
    max_abs = np.max(np.abs(vector))
    if max_abs == 0:
        return vector
    return vector / max_abs

normalized_vector = normalize_vector_max(theta_band_data[:,1])
theta_amplitude_zscore = stats.zscore(normalized_vector)


plt.figure(7)

plt.plot(theta_amplitude_zscore)
plt.title('Cepstrum  ifft(log(abs(fft(a))))')
plt.ylabel('z-score')
plt.xlabel('Quefrency(sec)')
#plt.axvline(8.5, color='limegreen', linewidth=100, alpha=0.4, zorder=0)
plt.grid(True)
plt.savefig('/Users/sarahtennant/Work_Alfredo/Analysis/Automatic_EEG_Analysis/figs/seiz_cepstrum-theta_zscore.png', dpi=200)
plt.draw()
plt.show()
