import Parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt
prm = Parameters.parameters()
import mne


# Set parameters
number_of_channels = 16
sample_rate = 250.4
sample_datatype = 'int16'
display_decimation = 1


#To set start and end times, put sample start and end below
start_sample=15054049
end_sample=36688608
tmin = start_sample/sample_rate
tmax = end_sample/sample_rate


# To load data, put file location and name below
recording = 'TAINI_1045_D_454redo_EOUBE_EM_3-2024_02_06-0001.dat'
filename = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/DATA/EOUBE/EOUBE_1045/' + recording
output_file = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/OUTPUT/EOUBE/EOUBE_1045/'




def load_dat(filename):

    '''Load a .dat file by interpreting it as int16 and then de-interlacing the 16 channels'''

    print("Loading_" + filename)

    # Load the raw (1-D) data
    dat_raw = np.fromfile(filename, dtype=sample_datatype)

    # Reshape the (2-D) per channel data
    step = number_of_channels * display_decimation
    dat_chans = [dat_raw[c::step] for c in range(number_of_channels)]

    # Build the time array
    t = np.arange(len(dat_chans[0]), dtype=float) / display_decimation
    data=np.array(dat_chans)
    print(len(data))
    del(dat_chans)
    n_channels=16
    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg']


    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, sample_rate, channel_types)


    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)

    return custom_raw



custom_raw = load_dat(filename)
custom_raw



# To do a basic plot below. The following can be added for specifc order of channels -- order=[4, 5, 3, 0, 1, 14, 15, 16]'

colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',

      emg='g', ref_meg='steelblue', misc='steelblue', stim='b',

     resp='k', chpi='k')



#Colour coded plot with start and end (ZT 0 to ZT 23)

#custom_raw.crop(tmin, tmax).plot(None, 60, 0, 16,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )

mne.viz.set_browser_backend('matplotlib', verbose=None)

fig = custom_raw.crop(tmin, tmax).plot(None, 60, 0, 16,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )
fig.savefig(output_file + 'eeg_snippet.png')

#Plot of all

#custom_raw.plot(None, 60, 0, 16, scalings = "auto", #order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true")



#Coloured coded plot of all and full recording

#custom_raw.plot(None, 60, 0, 16,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )#
