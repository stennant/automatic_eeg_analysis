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
    recording_length = 'int16'
    continuous_file_name = ''
    continuous_file_name_end = ''

    def __init__(self):
        return




    def get_is_ubuntu(self):
        return Parameters.is_ubuntu

    def set_is_ubuntu(self, is_ub):
        Parameters.is_ubuntu = is_ub

    def get_is_windows(self):
        return Parameters.is_windows

    def set_is_windows(self, is_win):
        Parameters.is_windows = is_win

    def get_sampling_rate(self):
        return Parameters.sampling_rate

    def set_sampling_rate(self, sr):
        Parameters.sampling_rate = sr

    def get_local_recording_folder_path(self):
        return Parameters.local_recording_folder_path

    def set_local_recording_folder_path(self, path):
        Parameters.local_recording_folder_path = path

    def get_file_path(self):
        return Parameters.file_path

    def set_file_path(self, path):
        Parameters.file_path = path

    def get_output_path(self):
        return Parameters.output_path

    def set_output_path(self, path):
        Parameters.output_path = path

    def get_number_of_channels(self):
        return Parameters.number_of_channels

    def set_number_of_channels(self, length):
        Parameters.number_of_channels = length

    def get_sample_datatype(self):
        return Parameters.sample_datatype

    def set_sample_datatype(self, in6):
        Parameters.sample_datatype = in6

    def get_recording_length(self):
        return Parameters.recording_length

    def set_recording_length(self, in6):
        Parameters.recording_length = in6

    def get_display_decimation(self):
        return Parameters.display_decimation

    def set_display_decimation(self, in6):
        Parameters.display_decimation = in6

    def get_start_sample(self):
        return Parameters.start_sample

    def set_start_sample(self, in6):
        Parameters.start_sample = in6

    def get_end_sample(self):
        return Parameters.end_sample

    def set_end_sample(self, in6):
        Parameters.end_sample = in6

    def get_continuous_file_name(self):
        return self.continuous_file_name

    def set_continuous_file_name(self, cont_name):
        Parameters.continuous_file_name = cont_name

    def get_continuous_file_name_end(self):
            return self.continuous_file_name_end

    def set_continuous_file_name_end(self, cont_name):
        Parameters.continuous_file_name_end = cont_name

