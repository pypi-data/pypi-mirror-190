from simba.read_config_unit_tests import read_config_file
import itertools
import pickle


class UMAPEmbedder(object):
    def __init__(self,
                 config_path: str,
                 data_path: str,
                 hyper_parameters: dict):

        self.config = read_config_file(ini_path=config_path)
        self.data_path, self.hyp = data_path, hyper_parameters
        self.search_space = list(itertools.product(*[self.hyp['n_neighbors'],
                                                     self.hyp['min_distance'],
                                                     self.hyp['dimensions']]))
        self.read()
        if self.hyp['scaler'] == 'STANDARD':
            self.standard_scaler()


    def read(self):
        with open(self.data_path, 'rb') as f:
            self.data_df = pickle.load(f)

    def standard_scaler(self):



hyper_parameters = {'n_neighbors': [10, 20], 'min_distance': [0, 1], 'dimensions': [2, 3], 'scaler': 'STANDARD'}
data_path = '/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/logs/unsupervised_data_20230206143248.pickle'
config_path = '/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini'

_ = UMAPEmbedder(config_path=config_path, data_path=data_path, hyper_parameters=hyper_parameters)