class Parameters:

    is_ubuntu = True
    is_windows = False
    sampling_rate = 0
    sample_datatype = 'int16'
    local_recording_folder_path = ''
    file_path = []
    output_path = []
    sorter_name = []
    number_of_channels = []
    display_decimation = []
    start_sample = []
    end_sample = []


    def __init__(self):
        return




    def get_is_ubuntu(self):
        return parameters.is_ubuntu

    def set_is_ubuntu(self, is_ub):
        parameters.is_ubuntu = is_ub

    def get_is_windows(self):
        return parameters.is_windows

    def set_is_windows(self, is_win):
        parameters.is_windows = is_win

    def get_sampling_rate(self):
        return parameters.sampling_rate

    def set_sampling_rate(self, sr):
        parameters.sampling_rate = sr

    def get_local_recording_folder_path(self):
        return parameters.local_recording_folder_path

    def set_local_recording_folder_path(self, path):
        parameters.local_recording_folder_path = path

    def get_file_path(self):
        return parameters.file_path

    def set_file_path(self, path):
        parameters.file_path = path

    def get_output_path(self):
        return parameters.output_path

    def set_output_path(self, path):
        parameters.output_path = path

    def get_number_of_channels(self):
        return parameters.number_of_channels

    def set_number_of_channels(self, length):
        parameters.number_of_channels = length

    def get_sample_datatype(self):
        return parameters.sample_datatype

    def set_sample_datatype(self, in6):
        parameters.sample_datatype = in6


    def get_display_decimation(self):
        return parameters.display_decimation

    def set_display_decimation(self, in6):
        parameters.display_decimation = in6

    def get_start_sample(self):
        return parameters.start_sample

    def set_start_sample(self, in6):
        parameters.start_sample = in6

    def get_end_sample(self):
        return parameters.end_sample

    def set_end_sample(self, in6):
        parameters.end_sample = in6
