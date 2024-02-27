import parameters
import mne
from pylab import *
from mne import io
import pandas as pd
import itertools


"""
This script does the following: 
1. loads raw EEG data using the MNE package 
2. Plot power spectra for all data
3. Load sleep score data
4. Split EEG data based on sleep score (i.e. WAKE, NREM, REM)
5. Calculate and plot power spectra for each sleep state

Channel map : 
EMG 1 --- 1 (this is 16 in 545)
EM-L --- 5
EV-L --- 8
EM-R --- 9
EV-R --- 10
"""

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
file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/DATA/EOUBE/EOUBE_454redo'
recording = '/TAINI_1045_D_454redo_EOUBE_EM_3-2024_02_06-0001.dat'
file_name = file_path + recording


# path to the sleep score output from R below
state_data_path = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/OUTPUT/EOUBE/EOUBE_454redo/EOUBE_1045_BL1-dge_swd.csv'


# load data file as RawArray using mne package
def load_dat(file_name):

    '''Load a .dat file by interpreting it as int16 and then de-interlacing the 16 channels'''

    print("Loading_" + file_name)

    # Load the raw (1-D) data
    dat_raw = np.fromfile(file_name, dtype=sample_datatype)

    # Reshape the (2-D) per channel data
    step = number_of_channels * display_decimation
    dat_chans = [dat_raw[c::step] for c in range(number_of_channels)]

    # Build the time array
    data=np.array(dat_chans)
    del(dat_chans)
    #channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_names=['1', '2', '3', '4', 'EM-L', '6', '7', 'EV-L', 'EM-R', 'EV-R', '11', '12', '13', '14', '15', 'EMG']
    channel_types=['misc','misc','misc','misc','eeg','misc','misc','eeg','eeg','eeg','misc','misc','misc','misc','misc','emg']

    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, sample_rate, channel_types)


    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)

    # For testing code, take only a small segment of the data
    #custom_raw = custom_raw.crop(tmin=0, tmax=60) # this is for testing
    #custom_raw.crop(tmin=0, tmax=60).plot()
    return custom_raw


# Create a label for the sleep data - currently unused
def label_sleep_data(data):
    data['event'] = ''

    # Define a function to map the values
    def set_value(row_number, assigned_value):
        return assigned_value[row_number]

    # Create the dictionary
    event_dictionary = {1: "Wake", 2: "NREM", 0: "REM"}

    # Add a new column named 'Price'
    data['event'] = data['sleep.score'].apply(set_value, args=(event_dictionary, ))
    return data


# Load sleep state score
def load_state_data(state_data_path):

    # Load sleep state score from .csv
    data = pd.read_csv(state_data_path, delimiter=",") # read .csv file with sleep score
    data['time'] = data.index # make column of time (index of the dataframe)
    data['duration'] = 5 # this column is needed for mne.Epochs function

    data = data[['time', 'duration', 'sleep.score']] # Take only these columns and in the order that is appropraite for mne.Epochs function [time stamp, duration, event label]
    return data


# calculate power spectra and plot
def power_spectra(custom_raw, state_data):

    # calculate the power spectra for all data using method = "welchs"
    custom_raw.compute_psd(method="welch", remove_dc = "True", average = False).plot(picks='eeg', average = False, spatial_colors = True)

    # Get sleep data in correct format for Epoch function - array of nested lists
    state_data_for_epochs = list(state_data.itertuples(index=False, name=None))

    # Get epochs for just wake times
    epoch_data = mne.Epochs(raw = custom_raw, events = state_data_for_epochs, event_id = dict(Wake=0, NREM =1, REM=2, SWD=4))
    #epoch_data.plot(picks = ['eeg', 'emg']) # plot epoch data

    # Subset data by sleep state
    psd_swd = epoch_data['SWD'].compute_psd(method="welch")
    psd_rem = epoch_data['REM'].compute_psd(method="welch")
    psd_nrem = epoch_data['NREM'].compute_psd(method="welch")
    psd_wake = epoch_data['Wake'].compute_psd(method="welch")

    # plot power spectra for wake
    axes = plt.subplot() # create your own axes object
    fig = psd_swd.plot(axes=axes, show=False, color = 'black', spatial_colors=False)
    fig = psd_rem.plot(axes=axes, show=False, color = 'blue', spatial_colors=False)
    fig = psd_nrem.plot(axes=axes, show=False, color = 'red', spatial_colors=False)
    fig = psd_wake.plot(axes=axes, show=False, color = 'green', spatial_colors=False)
    fig.axes[0].set_title("Sleep State Power Spectra's") # access the axes object and set the title
    plt.show()

    return custom_raw



custom_raw = load_dat(file_name)

state_data = load_state_data(state_data_path)

power_spectra(custom_raw, state_data)
