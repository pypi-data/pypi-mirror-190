import os, glob
import pandas as pd
from simba.read_config_unit_tests import (read_project_path_and_file_type,
                                          read_config_file,
                                          read_config_entry,
                                          check_if_filepath_list_is_empty,
                                          check_file_exist_and_readable)
from simba.train_model_functions import get_all_clf_names
from simba.misc_tools import get_fn_ext
from simba.drop_bp_cords import getBpNames
from simba.rw_dfs import read_df
from simba.enums import Paths, ReadConfig, Dtypes
from datetime import datetime
import pickle


class DatasetCreator(object):
    def __init__(self,
                 config_path: str,
                 settings: dict):

        self.config, self.settings = read_config_file(ini_path=config_path), settings
        self.config_path = config_path
        self.datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        self.project_path, self.file_type = read_project_path_and_file_type(config=self.config)
        self.logs_path = os.path.join(self.project_path, 'logs')
        self.save_path = os.path.join(self.logs_path, 'unsupervised_data_{}.pickle'.format(self.datetime))
        self.input_dir = os.path.join(self.project_path, Paths.MACHINE_RESULTS_DIR.value)
        self.files_found = glob.glob(f'{self.input_dir}/*.{self.file_type}')
        self.model_cnt = read_config_entry(self.config, ReadConfig.SML_SETTINGS.value, ReadConfig.TARGET_CNT.value, data_type=Dtypes.INT.value)
        self.clf_names = get_all_clf_names(config=self.config, target_cnt=self.model_cnt)
        self.clf_cols = ['Probability_' + x for x in self.clf_names] + self.clf_names
        check_if_filepath_list_is_empty(filepaths=self.files_found, error_msg='NO MACHINE LEARNING DATA FOUND')
        if settings['slice_type'] == 'ALL FEATURES (EXCLUDING POSE)':
            self.all_features_concatenator()
        if settings['slice_type'] == 'USER-DEFINED FEATURE SET':
            self.user_defined()
        self.save()

    def all_data_concatenator(self):
        self.df = []
        for file_path in self.files_found:
            _, video_name, _ = get_fn_ext(filepath=file_path)
            df = read_df(file_path=file_path,file_type=self.file_type)
            df.insert(0, 'FRAME', df.index)
            df.insert(0, 'VIDEO', video_name)
            self.df.append(df)
        self.df = pd.concat(self.df, axis=0).reset_index(drop=True)

    def all_features_concatenator(self):
        self.df = []
        bp_names = getBpNames(inifile=self.config_path)[0]
        for file_path in self.files_found:
            _, video_name, _ = get_fn_ext(filepath=file_path)
            df = read_df(file_path=file_path, file_type=self.file_type, remove_columns=bp_names)
            df.insert(0, 'FRAME', df.index)
            df.insert(0, 'VIDEO', video_name)
            self.df.append(df)
        self.df = pd.concat(self.df, axis=0).reset_index(drop=True)

    def user_defined(self):
        if not self.settings['feature_path']:
            print('Select a file path')
            raise FileNotFoundError('Select a feature file path')
        check_file_exist_and_readable(self.settings['feature_path'])
        feature_lst = list(pd.read_csv(self.settings['feature_path'], header=None)[0])
        self.df = []
        for file_path in self.files_found:
            _, video_name, _ = get_fn_ext(filepath=file_path)
            df = read_df(file_path=file_path, file_type=self.file_type, usecols=feature_lst + self.clf_cols)
            df.insert(0, 'FRAME', df.index)
            df.insert(0, 'VIDEO', video_name)
            self.df.append(df)
        self.df = pd.concat(self.df, axis=0).reset_index(drop=True)

    def save(self):
        self.results = {}
        self.results['ID'] = self.df[['FRAME', 'VIDEO']]
        self.results['CLF'] = self.df[self.clf_cols]
        self.results['DATA'] = self.df.drop(self.clf_cols + ['FRAME', 'VIDEO'], axis=1)
        with open(self.save_path, 'wb') as handle:
            pickle.dump(self.results, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('DATA SAVED')

# settings = {'slice_type': 'USER-DEFINED FEATURE SET', 'feature_path': '/Users/simon/Desktop/envs/simba_dev/simba/assets/unsupervised/features.csv'}
#
# _ = DatasetCreator(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
#                    settings=settings)

