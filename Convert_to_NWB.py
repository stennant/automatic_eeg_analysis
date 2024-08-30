# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:07:45 2020
Edited on 21/08/24 by Sarah Tennant

@author: Alfredo
"""

# import scripts
from initial_processes import *

'Below are imports for NWB'
from datetime import datetime
from uuid import uuid4

import numpy as np
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from pynwb.ecephys import LFP, ElectricalSeries
from pynwb.behavior import Position, SpatialSeries
from pynwb.file import Subject

'This section is for loading a subtime of a Tainitec DAT file'

number_of_channels = 16
sample_rate = 250.4
sample_datatype = 'int16'
display_decimation = 1

"Specifiy the start time and end times here!!!!"

start_time = 67370
end_time = 67380

fn = "/Users/sarahtennant/Work_Alfredo/Analysis/SCN2A/SCN2A_477/TAINI_1044_C_SCN2A_477_BL-2024_01_26-0000.dat"


def parse_dat(fn):
    '''Load a .dat file by interpreting it as int16 and then de-interlacing the 16 channels'''

    # Load the raw (1-D) data
    dat_raw = np.fromfile(fn, dtype=sample_datatype)

    # Reshape the (2-D) per channel data
    step = number_of_channels * display_decimation
    dat_chans = [dat_raw[c::step] for c in range(number_of_channels)]

    # Build the time array
    t = np.arange(len(dat_chans[0]), dtype=float) / sample_rate

    return dat_chans, t


dat_chans, t = parse_dat(fn)

data = np.array(dat_chans)
length = (len(data[0]))
print(length / sample_rate / 3600)
del (dat_chans)

datatp = data.transpose()

del (data)

sub_data = sub_time_data(datatp, start_time, end_time, sample_rate)

sub_datatp = sub_data.transpose()

sub_data_1 = sub_datatp[2]
#


'This section is to create the NWB file'

session_start_time = datetime(2024, 1, 26, 12, 51, 17, tzinfo=None)

nwbfile = NWBFile(
    session_description="Rat in home cage 24 hour recordings",  # required
    identifier="SCN2A_477",  # required
    session_start_time=session_start_time,  # required
    session_id=str(session_start_time),  # optional
    experimenter=[
        "McLaughlin, Niamh",
    ],  # optional
    lab="Gonzalez-Sulser Laboratory",  # optional
    institution="University of Edinburgh",  # optional
    experiment_description="Sleep-wake 24 hour recording home cage",  # optional
    keywords=["EEG", "Sleep", "Wake"],  # optional
    related_publications="https://doi.org/10.1101/2024.02.27.582289 ",  # optional
)
nwbfile

'This section creates electrodes'

device = nwbfile.create_device(
    name="array", description="Screw Electrode", manufacturer="RS Components"
)

nwbfile.add_electrode_column(name="label", description="label of electrode")

nshanks=1
nchannels = 1
electrode_counter = 0

for ishank in range(nshanks):
    # create an electrode group for this shank
    electrode_group = nwbfile.create_electrode_group(
        name="shank{}".format(ishank),
        description="electrode group for shank {}".format(ishank),
        device=device,
        location="brain area",
    )
    # add electrodes to the electrode table
    for ielec in range(nchannels):
        nwbfile.add_electrode(
            group=electrode_group,
            label="shank{}elec{}".format(ishank, ielec),
            location="brain area",
        )
        electrode_counter += 1


all_table_region = nwbfile.create_electrode_table_region(
    region=list(range(electrode_counter)),  # reference row indices 0 to N-1
    description="all electrodes",
)

'This section adds info about the subject recorded'
subject = Subject(
    subject_id="447",
    age="36 weeks",
    description="SCN2A 447",
    species="Rattus norvegicus",
    sex="M",
)

nwbfile.subject = subject
subject

time_series_with_rate = TimeSeries(
    name="test_timeseries",
    description="an example time series with a spike wave discharge",
    data=sub_data_1,
    unit="s",
    starting_time=0.0,
    rate=250.4,
)
time_series_with_rate

nwbfile.add_acquisition(time_series_with_rate)


io = NWBHDF5IO("SCN_477.nwb", mode="w")
io.write(nwbfile)
io.close()

