import parameters
import numpy as np
import pandas as pd
import mne
import matplotlib.pyplot as plt


prm = parameters.Parameters()


# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_local_recording_folder_path(recording_folder)
    prm.set_output_path(recording_folder)
    prm.set_sampling_rate(250)
    prm.set_number_of_channels(16)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)



def split_recording(file_path):

    input_df = np.fromfile(file_path, dtype=prm.get_sample_datatype())
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [input_df[c::step] for c in range(prm.get_number_of_channels())]

    # Build the time array
    data=np.array(dat_chans)

    del(dat_chans)
    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc']

    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)
    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)
    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    custom_raw.crop(5000,315100).plot(None, 1, 0,
                    order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options="true", block=True)


    eeg_data = pd.DataFrame(data)

    day1 = eeg_data.iloc[:,13792033:35426592]
    day2 = eeg_data.iloc[:,35426592:57061152]
    day3 = eeg_data.iloc[:,57061152:78695712]
    day4 = eeg_data.iloc[:,78695712:100330272]
    day5 = eeg_data.iloc[:,100330272:121964832]
    day6 = eeg_data.iloc[:,121964832:143599392]
    day7 = eeg_data.iloc[:,143599392:165233952]
    day8 = eeg_data.iloc[:,165233952:186868512]
    #day2 = eeg_data.iloc[:, 1250000:2250000]

    day1_values = day1.values.flatten()
    day2_values = day2.values.flatten()
    day3_values = day3.values.flatten()
    day4_values = day4.values.flatten()
    day5_values = day5.values.flatten()
    day6_values = day6.values.flatten()
    day7_values = day7.values.flatten()
    day8_values = day8.values.flatten()

    day1_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day1.dat')
    day2_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day2.dat')
    day3_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day3.dat')
    day4_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day4.dat')
    day5_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day5.dat')
    day6_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day6.dat')
    day7_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day7.dat')
    day8_values.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3687_Day8.dat')



def load_dat(file_name2):

    # Load the raw (1-D) data
    input_df = np.fromfile(file_name2, dtype=prm.get_sample_datatype())
    shape = np.shape(input_df)[0]/16
    output_df = np.reshape(input_df, (16,int(shape)))

    return output_df



def plot_raw(dat_raw, sampling_rate):
    channel_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types = ['emg', 'misc', 'misc', 'misc', 'misc', 'eeg', 'eeg', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc',
                     'misc', 'misc', 'misc']
    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, sampling_rate, channel_types)
    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(dat_raw, info)

    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    custom_raw.plot(None, 1, 0,
                    order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options="true", block=True)
    return



def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_name = '/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/TAINI_1048_SYNGAP_A_3686_EM11-2024_06_20-0000.dat'

    # set parameters
    parameters(file_name)

    split_recording(file_name)

    #check the .dat file
    #dat_filename2 = '/Users/sarahtennant/Work_Alfredo/Analysis/Lucy/SYNGAP_3686/3686_Day2.dat'
    #dat = load_dat(dat_filename2)
    #plot_raw(dat[:,:10000], 250)


if __name__ == '__main__':
    main()

