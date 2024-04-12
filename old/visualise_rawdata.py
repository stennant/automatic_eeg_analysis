import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt
import mne
import pandas as pd

prm = parameters.Parameters()


# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_local_recording_folder_path(recording_folder)
    prm.set_output_path(recording_folder)
    prm.set_sampling_rate(250.4)
    prm.set_number_of_channels(16)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)



def load_and_calculate_start_and_end_time(csv_path, animal_id):
    # Load start and end recording time from .csv
    data = pd.read_csv(csv_path, delimiter=",") # read .csv file with sleep score
    rat_data = data.loc[data['ratname'] == animal_id]
    start = rat_data.at[0,"startA"]
    end = rat_data.at[0,"endA"]
    prm.set_start_sample(start)
    prm.set_end_sample(end)
    return


def process_dir(file_name):
    # Load the raw (1-D) data
    dat_raw = np.fromfile(file_name, dtype=prm.get_sample_datatype())

    # Reshape the (2-D) per channel data
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [dat_raw[c::step] for c in range(prm.get_number_of_channels())]

    # Build the time array
    data=np.array(dat_chans)

    del(dat_chans)
    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg']


    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)


    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)

    return custom_raw



def plot_raw(eeg_data,file_name):

    mne.viz.set_browser_backend('matplotlib', verbose=None)


    #To set start and end times, put sample start and end below
    tmin = prm.get_start_sample()/prm.get_sampling_rate()
    tmax = prm.get_end_sample()/prm.get_sampling_rate()

    # To do a basic plot below. The following can be added for specifc order of channels -- order=[4, 5, 3, 0, 1, 14, 15, 16]'
    colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m', emg='g', ref_meg='steelblue', misc='steelblue', stim='b', resp='k', chpi='k')

    fig = eeg_data.crop(tmin, tmax).plot(None, 60, 0, 16,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )
    fig.savefig(file_name + 'eeg_snippet.png')





def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_176923/' # for syngape8 rats
    recording =  'TAINI_1044_176923-EM3-2024_03_27-0000.dat' # for rat 176923
    animal_id = file_path.rsplit("/", 3)[2]

    file_name = file_path + recording
    parameters(file_path)
    print('Processing ' + str(file_path + recording))

    #path to the csv with start and end times
    csv_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/rat_day_index_SYNGAPE8.csv'

    #set path to save data
    output_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Figures'
    # if the output path does not exist, make it
    if os.path.exists(output_path) is False:
        os.makedirs(output_path)

    # load the start and end time
    load_and_calculate_start_and_end_time(csv_path, animal_id)

    # LOAD DATA
    eeg_data = process_dir(file_name) # overall data

    # PLOT DATA
    plot_raw(eeg_data, output_path)



if __name__ == '__main__':
    main()

