import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import mne
import pandas as pd

import sleep_analysis
import detect_swd

recording_folder = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_176923/TAINI_1044_176923-EM3-2024_03_27-0000.dat' # for syngape8 rats
csv_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/rat_day_index_SYNGAPE8.csv'
output_figure_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Figures'
output_data_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Data_output'

# set eeg and emg channels
eeg_channels = [5, 8, 9, 10]
all_channels = [5, 8, 9, 10, 1]
main_eeg = 5

# set whether it will run SWD and or sleep analysis
SWD = True
sleep_analysis = True

prm = parameters.Parameters()

# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_sampling_rate(250.4)
    prm.set_number_of_channels(16)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)


def make_folder_structure(output_figure_path, output_data_path):
    # if the output path does not exist, make it
    if os.path.exists(output_figure_path) is False:
        os.makedirs(output_figure_path)
    if os.path.exists(output_data_path) is False:
        os.makedirs(output_data_path)


def load_start_and_end_time(csv_path):
    # Load start and end recording time from .csv
    animal_id = recording_folder.rsplit("/", 3)[2]

    data = pd.read_csv(csv_path, delimiter=",") # read .csv file with sleep score
    rat_data = data.loc[data['ratname'] == animal_id]
    start = rat_data.at[0,"startA"]
    end = rat_data.at[0,"endA"]
    prm.set_start_sample(start)
    prm.set_end_sample(end)
    return animal_id


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


def crop_by_start_and_end(custom_raw):
    #custom_raw = custom_raw.crop(prm.get_start_sample(), prm.get_end_sample()) # take full 24 hour recording
    custom_raw = custom_raw.crop(0, 1000) # testing dataset
    return custom_raw


def filter_data(custom_raw):
    print('Applying highpass filter to data....')
    filtered_data = custom_raw.filter(l_freq=0.2, h_freq=120, picks = all_channels) # filter the data between 0.2 to 120 Hz
    return filtered_data


def fill_outliers(filtered_data):
    print('Removing outliers from data....')
    data = filtered_data.to_data_frame()
    return filtered_data


def save_main_eeg_channel_as_csv(filtered_data, animal_id):
    print('Saving channel ' + str(main_eeg) + ' to csv file....')
    data = filtered_data.to_data_frame()
    main_eeg_channel = data[["time", str(main_eeg)]]
    main_eeg_channel.to_csv(output_data_path + '/' + str(animal_id) + 'channnels.csv', index=False)
    main_eeg_channel



def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')
    print('Processing ' + str(recording_folder))

    parameters(recording_folder)

    make_folder_structure(output_figure_path, output_data_path)

    animal_id = load_start_and_end_time(csv_path)

    custom_raw = process_dir(recording_folder)

    custom_raw = crop_by_start_and_end(custom_raw)


    # Now run specific analysis
    ### Note!!! Sleep detection analysis runs on filtered data, SWD analysis runs on raw data!!!

    if sleep_analysis == True:

        filtered_data = filter_data(custom_raw)

        main_eeg_channel = save_main_eeg_channel_as_csv(filtered_data, animal_id)

        sleep_data = sleep_analysis.run_sleep_analysis(main_eeg_channel)


    if SWD == True:

        swd_data = detect_swd.run_swd_detection(custom_raw)


if __name__ == '__main__':
    main()

