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


def split_recording(file_path):

    print("loading recording")

    input_df = np.fromfile(file_path, dtype=prm.get_sample_datatype())
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [input_df[c::step] for c in range(prm.get_number_of_channels())]

    data=np.array(dat_chans) # Build the time array
    del(dat_chans)

    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc']

    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types) # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    custom_raw = mne.io.RawArray(data, info) # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object

    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    # uncomment plot function below if you want to check the recording file before you split and save!!
    #custom_raw.crop(55080,141480).plot(None, 1, 0,
                    #order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options="true", block=True)

    eeg_data = pd.DataFrame(data) # convert mda file to a dataframe

    print("splitting recording")

    # split the recording into 8 days
    # NOTE: the indicies used to split the recording were calculated by taking the start sample (i.e. 7 am on the first day) and adding 24 hours of samples
    day1 = eeg_data.iloc[:,13792033:35426592]
    day2 = eeg_data.iloc[:,35426592:57061152]
    day3 = eeg_data.iloc[:,57061152:78695712]
    day4 = eeg_data.iloc[:,78695712:100330272]
    day5 = eeg_data.iloc[:,100330272:121964832]
    day6 = eeg_data.iloc[:,121964832:143599392]
    day7 = eeg_data.iloc[:,143599392:165233952]
    day8 = eeg_data.iloc[:,165233952:186868512]

    # flatten the values i.e. into one long array
    day1_values = day1.values.flatten('F')
    day2_values = day2.values.flatten('F')
    day3_values = day3.values.flatten('F')
    day4_values = day4.values.flatten('F')
    day5_values = day5.values.flatten('F')
    day6_values = day6.values.flatten('F')
    day7_values = day7.values.flatten('F')
    day8_values = day8.values.flatten('F')

    print("saving data")

    # save each array into a .dat file
    day1_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day1.dat')
    day2_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day2.dat')
    day3_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day3.dat')
    day4_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day4.dat')
    day5_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day5.dat')
    day6_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day6.dat')
    day7_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day7.dat')
    day8_values.astype('int16').tofile('/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day8.dat')


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

    #path to the recording .dat file
    file_name = '/Volumes/Sarah/Lucy/SYNGAP_3686/TAINI_1048_SYNGAP_A_3686_EM11-2024_06_20-0000.dat'

    # set parameters
    parameters(file_name)

    # function to split recording
    split_recording(file_name)

    #check the .dat file
    dat_filename = '/Volumes/Sarah/Lucy/SYNGAP_3686/3686_Day1.dat'
    plot_raw(dat_filename, 250.4)


if __name__ == '__main__':
    main()

