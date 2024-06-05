import parameters
import mne
from pylab import *
from mne import io
import pandas as pd
import itertools
import os


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
start_sample=128304
end_sample=344650
tmin = start_sample/sample_rate
tmax = end_sample/sample_rate


# To load data, put file location and name below
file_path = '/Volumes/Sarah/GNU/DATA/GNU/GNU_702'
recording = '/TAINI_1048_702_EM3-2024_04_15-0000.dat'

file_name = file_path + recording

output_path = '/Volumes/Sarah/GNU/DATA/GNU/GNU_702'

# if the output path does not exist, make it
if os.path.exists(output_path) is False:
    os.makedirs(output_path)

# path to the sleep score output from R below
state_data_path = '/Volumes/Sarah/GNU/OUTPUT/GNU/GNU_702/GNU_702_BL1-dge_swd.csv'

# Assign colors to each channel of raw EEG
colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',emg='g', ref_meg='steelblue', misc='steelblue', stim='b',resp='k', chpi='k')

# Assign labels to sleep score
event_id = {"Wake":0, "NREM":1, "REM":2, "SWD":4}  # Assign labels to sleep score


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
    channel_names=['EMG', '2', '3', '4', 'EM-L', '6', '7', 'EV-L', 'EM-R', 'EV-R', '11', '12', '13', '14', '15', '16']
    channel_types=['emg','misc','misc','misc','eeg','misc','misc','eeg','eeg','eeg','misc','misc','misc','misc','misc','misc']

    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, sample_rate, channel_types)


    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)

    # For testing code, take only a small segment of the data
    #custom_raw = custom_raw.crop(tmin=0, tmax=60) # this is for testing
    #custom_raw = custom_raw.crop(tmin, tmax) # take full 24 hour recording
    return custom_raw


# Create a label for the sleep data - currently unused
def label_sleep_data(data):
    data['description'] = ''

    # Define a function to map the values
    def set_value(row_number, assigned_value):
        return assigned_value[row_number]

    # Create the dictionary
    event_dictionary = {0: "Wake", 1: "NREM", 2: "REM", 4: "SWD"}

    # Add a new column named 'Price'
    data['description'] = data['sleep.score'].apply(set_value, args=(event_dictionary, ))
    return data


# Load sleep state score
def load_state_data(state_data_path):

    # Load sleep state score from .csv
    data = pd.read_csv(state_data_path, delimiter=",") # read .csv file with sleep score
    data['onset'] = data.index*5 # make column of time (index of the dataframe)
    data['duration'] = 5 # set duration of event - set as 5 since the sleep score is calculated in epochs of 5 seconds

    data = label_sleep_data(data) # label the sleep score

    # Get sleep data in correct format for Epoch function - array of nested lists
    annotations = mne.Annotations(onset = np.asarray(data["onset"]), duration = np.asarray(data["duration"]),description = np.asarray(data["description"]))

    return annotations


def view_annotations(custom_raw, events, event_id):
    annotated_custom_raw = custom_raw.copy().set_annotations(events)
    events_from_annot, event_dict = mne.events_from_annotations(annotated_custom_raw, event_id = event_id )
    return annotated_custom_raw, events_from_annot


def plot_events_on_raw(custom_raw, events_from_annot, event_id):
    #event_color_dictionary = {0: "green", 1: "red", 2: "blue", 4: "black"}
    #event_color_dictionary = {"Wake": "green", "NREM": "red", "REM": "blue", "SWD": "black"}
    custom_raw.plot(events=events_from_annot, duration=60, start=0, n_channels=16, color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" , event_id = event_id)
    return


# calculate power spectra and plot
def power_spectra_by_state(custom_raw, annotated_custom_raw, array_events, event_id):

    # calculate the power spectra for all data using method = "welchs"
    #custom_raw.compute_psd(method="welch", remove_dc = "True", average = False).plot(picks='eeg', average = False, spatial_colors = True)

    # Get epochs for just wake times
    epoch_data = mne.Epochs(raw = annotated_custom_raw, events = array_events, event_id = event_id, tmin=-0.1, tmax = 4.9)
    #epoch_data.plot(picks = ['eeg', 'emg']) # plot epoch data

    # Visualise raw epoched data with events
    #epoch_data.compute_psd(method='welch', picks='eeg', average=False, exclude='bads').plot(picks = 'eeg', spatial_colors=True)

    # Subset data by sleep state
    psd_swd = epoch_data['SWD'].compute_psd(method='welch', fmax=50, exclude='bads', picks=[5,8], average='mean').average()
    psd_rem = epoch_data['REM'].compute_psd(method='welch', fmax=50,  exclude='bads', picks=[5,8], average='mean').average()
    psd_nrem = epoch_data['NREM'].compute_psd(method='welch', fmax=50, exclude='bads', picks=[5,8], average='mean').average()
    psd_wake = epoch_data['Wake'].compute_psd(method='welch', fmax=50, exclude='bads', picks=[5,8], average='mean').average()

    # plot power spectra for wake
    pw_spec = plt.figure(figsize=(3.7,3))
    ax = pw_spec.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)

    swd = psd_swd.plot(axes=ax, show=False, color = 'black', spatial_colors=False, average=True)
    rem = psd_rem.plot(axes=ax, show=False, color = 'blue', spatial_colors=False, average=True)
    nrem = psd_nrem.plot(axes=ax, show=False, color = 'red', spatial_colors=False, average=True)
    wake = psd_wake.plot(axes=ax, show=False, color = 'green', spatial_colors=False, average=True)
    ax.set_title("Sleep State Power Spectra's") # access the axes object and set the title
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.legend([swd, rem, nrem, wake], ['SWD', 'REM', 'NREM', "Wake"])
    plt.show()
    plt.savefig(output_path + 'power_spec_by_state' + '.png', dpi=200)
    #plt.close()
    return custom_raw



custom_raw = load_dat(file_name)

annotations = load_state_data(state_data_path)

annotated_custom_raw, events_from_annot = view_annotations(custom_raw, annotations, event_id)

plot_events_on_raw(custom_raw, events_from_annot, event_id)

power_spectra_by_state(custom_raw,annotated_custom_raw, events_from_annot, event_id)
