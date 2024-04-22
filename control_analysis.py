import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import time
import mne
import pandas as pd
import matplotlib.pyplot as plt

import read_yaml_config
import sleep_analysis
import detect_swd


recording_folder = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_176923/TAINI_1044_176923-EM3-2024_03_27-0000.dat' # for syngape8 rats
configuration_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_176923/TAINI_1044_176923-EM3-2024_03_27-0000_configuration.yaml' # for syngape8 rats
output_figure_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Figures'
output_data_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Data_output'

# set eeg and emg channels - this is done from using the check_rawdata.py script
eeg_channels = [5, 8, 9, 10]
all_channels = [5, 8, 9, 10, 1]
main_eeg = 5

# set whether it will run SWD and or sleep analysis
SWD = True
sleep = False


prm = parameters.Parameters()

# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_sampling_rate(250.4)
    prm.set_number_of_channels(16)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)


def make_folder_structure(output_figure_path, output_data_path):
    if os.path.exists(output_figure_path) is False:
        os.makedirs(output_figure_path)
    if os.path.exists(output_data_path) is False:
        os.makedirs(output_data_path)

"""
def get_tags_parameter_file(recording_directory):
    tags = False
    parameters_path = recording_directory + '/parameters.txt'
    param_file_reader = open(parameters_path, 'r')
    parameters = param_file_reader.readlines()
    parameters = list([x.strip() for x in parameters])
    if len(parameters) > 2:
        tags = parameters[2]
    return tags
"""

def process_dir(file_name):
    print('Loading .dat file....')

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


def plot_interactive(custom_raw):
    import matplotlib.pyplot as plt
    plt.switch_backend('TkAgg') # need this for plotting interactive plot
    plt.ion() # need this for plotting interactive plot
    custom_raw.plot(None, 60, 0, 16, scalings = "auto", order=[4,7,8,9,10,15], show_options = "true" )


def crop_by_start_and_end(custom_raw):
    print('Cropping recording based on start and end times....')
    #plot_interactive(custom_raw)

    #custom_raw = custom_raw.crop(prm.get_start_sample(), prm.get_end_sample()) # take full 24 hour recording
    cropped_raw = custom_raw.crop(52182, 52812) # testing dataset - 52800, 52805 for seizure, 52910, 52915 for non seizure, 52782, 52812 for both
    return cropped_raw



def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')
    print('Processing ' + str(recording_folder))

    start = time.process_time() # so I can measure the time it takes for code to run

    animal_id = recording_folder.rsplit("/", 3)[2]

    parameters(recording_folder)

    make_folder_structure(output_figure_path, output_data_path)

    read_yaml_config.calculate_recording_duration(configuration_path) # set start and end time by extracting from the configuration file

    custom_raw = process_dir(recording_folder)

    cropped_raw = crop_by_start_and_end(custom_raw)


    # Now run specific analysis
    if sleep == True:

        sleep_analysis.run_sleep_analysis(cropped_raw, animal_id, all_channels, main_eeg, output_data_path, output_figure_path)

    if SWD == True:

        detect_swd.run_swd_detection(cropped_raw, all_channels, main_eeg, output_data_path, output_figure_path)

    end_time = time.process_time() - start

    print('I have processed ' + str(recording_folder))
    print('Data is saved in ' + str(output_data_path))
    print('Figures are saved in ' + str(output_figure_path))
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    print('code took ' + str(end_time) + ' to run')


if __name__ == '__main__':
    main()

