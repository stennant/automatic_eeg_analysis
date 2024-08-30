from pynwb import NWBHDF5IO, NWBFile, TimeSeries


filepath = "SCN_477.nwb"
# Open the file in read mode "r",
io = NWBHDF5IO(filepath, mode="r")
nwbfile = io.read()
nwbfile

nwbfile.TimeSeries.to_dataframe()