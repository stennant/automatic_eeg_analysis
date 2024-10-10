import parameters
import numpy as np
import pandas as pd
import mne
import matplotlib.pyplot as plt

prm = parameters.Parameters()


# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_sampling_rate(250.4)
    prm.set_number_of_channels(16)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)

def load_recording(file_path):

    input_df = np.fromfile(file_path, dtype=prm.get_sample_datatype())
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [input_df[c::step] for c in range(prm.get_number_of_channels())]

    data=np.array(dat_chans) # Build the time array
    del(dat_chans)

    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc']

    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types) # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    custom_raw = mne.io.RawArray(data, info) # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    return custom_raw, data

def merge_recording(file_path_1, file_path_2):

    print("loading recordings ...")

    custom_raw_1, data_1 = load_recording(file_path_1)
    custom_raw_2, data_2 = load_recording(file_path_2)

    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    # uncomment plot function below if you want to check the recording file before you split and save!!
    custom_raw_1.crop(0,1000).plot(None, 1, 0, order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options="true", block=True)


    print("merging recording")

    merged_data = np.concatenate((data_1, data_2), axis=1)
    merged_data = pd.DataFrame(merged_data) # convert mda file to a dataframe

    print("saving data")

    # flatten the values i.e. into one long array
    eeg_data_values = merged_data.values.flatten('F')

    # save each array into a .dat file
    eeg_data_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/SCN2A/SCN2A_477/test_merge.dat')



'''
this is for checking the saved data files
'''
def plot_raw(file_path, sampling_rate):
    input_df = np.fromfile(file_path, dtype=prm.get_sample_datatype())
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [input_df[c::step] for c in range(prm.get_number_of_channels())]

    data=np.array(dat_chans)
    del(dat_chans)

    channel_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types = ['emg', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc',
                     'misc', 'misc', 'misc']
    info = mne.create_info(channel_names, sampling_rate, channel_types)
    custom_raw = mne.io.RawArray(data, info)

    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    custom_raw.crop(0,1000).plot(None, 1, 0,
                    order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options="true", block=True)
    return




def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the two recording .dat files you want to merge
    file_name_1 = '/Users/sarahtennant/Work_Alfredo/Analysis/SCN2A/SCN2A_477/TAINI_1044_C_SCN2A_477_BL-2024_01_26-0000.dat'
    file_name_2 = '/Users/sarahtennant/Work_Alfredo/Analysis/SCN2A/SCN2A_477/TAINI_1044_C_SCN2A_477_BL-2024_01_26-0000.dat'

    # set parameters
    parameters(file_name_1)

    # function to split recording
    merge_recording(file_name_1, file_name_2)

    #check the .dat file
    dat_filename = '/Users/sarahtennant/Work_Alfredo/Analysis/SCN2A/SCN2A_477/test_merge.dat'
    plot_raw(dat_filename, 250.4)


if __name__ == '__main__':
    main()

