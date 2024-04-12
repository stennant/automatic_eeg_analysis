import sys
import os.path
import numpy as np
from numpy import *
import parameters
import os
import matplotlib.pyplot as plt
prm = parameters.Parameters()
from OpenEphys import *
import mne
import xlrd
import numpy as np
mne.viz.set_browser_backend('matplotlib', verbose=None)
import pandas as pd

number_of_channels = 16
sample_rate = 250.4
sample_datatype = 'int16'
display_decimation = 1

"To set start and end times, put sample start and end below"

start_sample=18209089
end_sample=39843648

#start_sample=33849073
#end_sample=55483632c


tmin = start_sample/sample_rate
tmax = end_sample/sample_rate

"To load the data, put file location and name below using double back to front slash"

filename="C:\\Users\\niamh\\OneDrive\\Desktop\\SCN2A_EEG\\BL\\SCN2A\\SCN2A_476\\TAINI_1048_A_SCN2A_476_BL-2024_02_05-0000.dat"

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

    channel_names=['1', '2', '3', '4', '5',
                           '6', '7', '8', '9', '10',
                           '11', '12', '13', '14', '15', '16']
    channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','misc','misc','misc','eeg']
#Transmitter C
   # channel_types=['emg','emg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','misc','eeg']


    'This creates the info that goes with the channels, which is names, sampling rate, and channel types.'
    info = mne.create_info(channel_names, sample_rate, channel_types)


    'This makes the object that contains all the data and info about the channels.'
    'Computations like plotting, averaging, power spectrums can be performed on this object'

    custom_raw = mne.io.RawArray(data, info)

    return custom_raw

custom_raw = load_dat(filename)


"Makes basic, colour coded plot for annotation"
colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',
      emg='g', ref_meg='steelblue', misc='steelblue', stim='b',
     resp='k', chpi='k')


custom_raw.crop(tmin, tmax).plot(None, 60, 0, 16, color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true")

"Save annotations once finished"
def save_annotation ():
    custom_raw.annotations.save(str("476_saved-annotations.txt"), overwrite=True) #change me


"Basic plot with annotations (update .txt file)"
"only run once for each file"
def update_annotations_for_plotting():
    "Modify annotation file (.txt) to save and plot annotations in future sessions"
    annot_file = pd.read_table("476_saved-annotations.txt", #change me
         delimiter=',',
         skiprows=2,
         header=None)

    adapt_first_column = annot_file[annot_file.columns[0]] - tmin
    annot_file[annot_file.columns[0]] = adapt_first_column


    WorkingFolder = "C:\MNE_Alfredo_update"
    base_filename = "476_saved-annotations.txt" #change me
    with open(os.path.join(WorkingFolder, base_filename),'w') as outfile:
        annot_file.to_csv("476_saved-annotations.txt", index=False, sep=",", header=False)
    line1 = "# MNE-Annotations"
    line2 = "# onset, duration, description"
    with open("476_saved-annotations.txt", 'r+') as file: #change me
        file_data = file.read()
        file.seek(0, 0)
        file.write(line1 + '\n' + line2 + '\n' + file_data)
    print("No need to update onset values now")


def annotated_plot(annotated_file):
    manual_annotations = mne.read_annotations("476_saved-annotations.txt", sfreq=250.4)
    #annotated_custom_raw = custom_raw.copy().crop(tmin, tmax).set_annotations(manual_annotations)
    annotated_custom_raw = custom_raw.copy().set_annotations(manual_annotations)
    annotated_custom_raw.crop(tmin,tmax).plot(None, 60, 0, 16, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true")

"Create .png of EEG using matplotlib saving function, given x-axis"
#fig = annotated_custom_raw.plot(None, 60, 0, 16, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true")
#fig.savefig("C:\\Users\\niamh\\OneDrive\\Desktop\\SCN2A_EEG\\BL\\SCN2A\\SCN2A_445")

"Save annotations once finished"
def save_edited_annotation ():
    annotated_custom_raw.annotations.save(str("476_saved-annotations.txt"), overwrite=True) #change me


"convert annotations to events"
annotated_file = "476_saved-annotations.txt"
manual_annotations = mne.read_annotations("476_saved-annotations.txt")
annotated_custom_raw = custom_raw.copy().set_annotations(manual_annotations)
events = mne.events_from_annotations(annotated_custom_raw)
array_events = list(events[0])


"plot and examine"
mne.viz.plot_events(array_events, sfreq=250.4, first_samp=annotated_custom_raw.first_samp)
#mne.viz.plot_events(array_events, sfreq=250.4)

"create epochs around events"
full_custom_raw = load_dat(filename)
annotated_full_custom_raw = full_custom_raw.copy().set_annotations(manual_annotations)

event_id = {"Unlabelled SWD": 1, "Labelled SWD":2}

epochs = mne.Epochs(annotated_full_custom_raw, array_events, event_id, tmin=-0.1, tmax=4.9)
epochs.plot(picks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

"plotting power spectrum of epochs"

labelled_SWD_epoch_spectrum = epochs['Labelled SWD'].compute_psd(method="welch", picks=16).plot()


#plt.title("Labelled SWD Epoch Power Spectrum (PSD) ")
#plt.psd(labelled_SWD_epoch_spectrum)

#unlabelled_SWD_epoch_spectrum = epochs['Unlabelled SWD'].compute_psd(method="welch", picks="eeg").plot()
#plt.title("Unlabelled SWD Epoch Power Spectrum (PSD) ")
