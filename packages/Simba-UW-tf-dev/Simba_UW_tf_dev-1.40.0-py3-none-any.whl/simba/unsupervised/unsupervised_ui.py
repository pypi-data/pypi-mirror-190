from simba.read_config_unit_tests import (read_config_entry,
                                          read_config_file,
                                          read_project_path_and_file_type,
                                          check_float)
from tkinter import *
from simba.tkinter_functions import hxtScrollbar, Entry_Box, DropDownMenu, FileSelect
import tkinter.ttk as ttk
from simba.enums import Formats
from simba.unsupervised.dataset_creator import DatasetCreator

class UnsupervisedGUI(object):
    def __init__(self,
                 config_path: str):

        self.config = read_config_file(config_path)
        self.project_path, self.file_type = read_project_path_and_file_type(config=self.config)
        self.main = Toplevel()
        self.main.minsize(1300, 800)
        self.main.wm_title("UNSUPERVISED ANALYSIS")
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(0, weight=1)
        self.data_slice_options = ['ALL FEATURES (EXCLUDING POSE)',
                                   'ALL FEATURES (INCLUDING POSE)',
                                   'USER-DEFINED FEATURE SET']
        self.normalization_options = ['STANDARD',
                                      'QUANTILE',
                                      'MIN-MAX']
        self.algo_options = ['UMAP',
                             'PCA',
                             'TSNE']


        self.feature_removal_options = list(range(0, 100, 10))
        self.feature_removal_options = [str(x) + '%' for x in self.feature_removal_options]
        self.main = ttk.Notebook(hxtScrollbar(self.main))
        self.create_dataset_tab = ttk.Frame(self.main)
        self.dimensionality_reduction_tab = ttk.Frame(self.main)
        self.main.add(self.create_dataset_tab, text=f'{"[CREATE DATASET]": ^20s}')
        self.main.add(self.dimensionality_reduction_tab, text=f'{"[DIMENSIONALITY REDUCTION]": ^20s}')
        self.main.grid(row=0)

        create_dataset_frm = LabelFrame(self.create_dataset_tab, text='CREATE DATASET', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.feature_file_selected = FileSelect(create_dataset_frm, "FEATURE FILE (CSV)")
        self.feature_file_selected.entPath.config(state='disabled')
        self.data_slice_dropdown = DropDownMenu(create_dataset_frm, 'DATA SLICE:', self.data_slice_options, '12', com= lambda x: self.change_state_feature_file_selected())
        self.data_slice_dropdown.setChoices(self.data_slice_options[0])
        self.create_btn = Button(create_dataset_frm, text='CREATE DATASET', fg='blue', command= lambda: None)
        create_dataset_frm.grid(row=0, column=0, sticky=NW)
        self.data_slice_dropdown.grid(row=0, column=0, sticky=NW)
        self.feature_file_selected.grid(row=1, column=0, sticky=NW)
        self.create_btn.grid(row=2, column=0, sticky=NW)


        self.dim_reduction_frm = LabelFrame(self.dimensionality_reduction_tab, text='DIMENSIONALITY REDUCTION', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.dataset_frm = LabelFrame(self.dimensionality_reduction_tab, text='DATASET', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.feature_file_selected = FileSelect(self.dataset_frm, "DATASET (PICKLE): ")
        settings_frm = LabelFrame(self.dim_reduction_frm, text='SETTINGS', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.data_slice_dropdown = DropDownMenu(settings_frm, 'SCALING:', self.normalization_options, '12')
        self.data_slice_dropdown.setChoices(self.normalization_options[0])
        self.feature_removal_dropdown = DropDownMenu(settings_frm, 'VARIANCE:', self.feature_removal_options, '12')
        self.feature_removal_dropdown.setChoices(self.feature_removal_options[0])
        choose_algo_frm = LabelFrame(self.dim_reduction_frm, text='ALGORITHM', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.choose_algo_dropdown = DropDownMenu(settings_frm, 'ALGORITHM:', self.algo_options, '12', com=lambda x: self.show_algo_hyperparameters())
        self.choose_algo_dropdown.setChoices(self.algo_options[0])
        self.dim_reduction_frm.grid(row=0, column=0, sticky=NW)
        settings_frm.grid(row=0, column=0, sticky=NW)
        self.data_slice_dropdown.grid(row=1, column=0, sticky=NW)
        self.feature_removal_dropdown.grid(row=2, column=0, sticky=NW)
        choose_algo_frm.grid(row=1, column=0, sticky=NW)
        self.choose_algo_dropdown.grid(row=0, column=0, sticky=NW)

        self.main.mainloop()
    def show_algo_hyperparameters(self):
        if hasattr(self, 'hyperparameters_frm'):
            self.hyperparameters_frm.destroy()

        if self.choose_algo_dropdown.getChoices() == 'UMAP':
            self.hyperparameters_frm = LabelFrame(self.dim_reduction_frm, text='GRID SEARCH HYPER-PARAMETERS', pady=5, padx=5, font=Formats.LABELFRAME_HEADER_FORMAT.value, fg='black')
            self.value_frm = LabelFrame(self.dim_reduction_frm, fg='black')
            self.value_entry_box = Entry_Box(self.value_frm, 'VALUE: ', '12')
            n_neighbors_estimators_lbl = Label(self.hyperparameters_frm, text='N NEIGHBOURS')
            min_distance_lbl = Label(self.hyperparameters_frm, text='MIN DISTANCE')
            dimensions_lbl = Label(self.hyperparameters_frm, text='DIMENSION')
            add_min_distance_btn = self.create_btn = Button(self.hyperparameters_frm, text='ADD', fg='blue', command= lambda: self.add_to_listbox(list_box=self.min_distance_listb))
            add_dimensions_btn = self.create_btn = Button(self.hyperparameters_frm, text='ADD', fg='blue', command=lambda: self.add_to_listbox(list_box=self.n_dimensions_listb))
            add_neighbours_btn = self.create_btn = Button(self.hyperparameters_frm, text='ADD', fg='blue', command=lambda: self.add_to_listbox(list_box=self.n_neighbors_estimators_listb))
            remove_min_distance_btn = self.create_btn = Button(self.hyperparameters_frm, text='REMOVE', fg='red', command= lambda: self.remove_from_listbox(list_box=self.min_distance_listb))
            remove_dimensions_btn = self.create_btn = Button(self.hyperparameters_frm, text='REMOVE', fg='red', command=lambda: self.remove_from_listbox(list_box=self.n_dimensions_listb))
            remove_neighbours_btn = self.create_btn = Button(self.hyperparameters_frm, text='REMOVE', fg='red', command=lambda: self.remove_from_listbox(list_box=self.n_neighbors_estimators_listb))
            self.n_neighbors_estimators_listb = Listbox(self.hyperparameters_frm, bg='lightgrey', fg='black', height=5, width=15)
            self.n_dimensions_listb = Listbox(self.hyperparameters_frm, bg='lightgrey', fg='black', height=5, width=15)
            self.min_distance_listb = Listbox(self.hyperparameters_frm, bg='lightgrey', fg='black', height=5, width=15)
            self.value_frm.grid(row=3, column=0, sticky=NW)
            self.value_entry_box.grid(row=0, column=1, sticky=NW)
            self.hyperparameters_frm.grid(row=4, column=0, sticky=NW)
            n_neighbors_estimators_lbl.grid(row=1, column=0)
            min_distance_lbl.grid(row=1, column=1)
            dimensions_lbl.grid(row=1, column=2)
            add_neighbours_btn.grid(row=2, column=0)
            add_dimensions_btn.grid(row=2, column=1)
            add_min_distance_btn.grid(row=2, column=2)
            remove_neighbours_btn.grid(row=3, column=0)
            remove_dimensions_btn.grid(row=3, column=1)
            remove_min_distance_btn.grid(row=3, column=2)
            self.n_neighbors_estimators_listb.grid(row=4, column=0, sticky=NW)
            self.n_dimensions_listb.grid(row=4, column=1, sticky=NW)
            self.min_distance_listb.grid(row=4, column=2, sticky=NW)

    def change_state_feature_file_selected(self):
        if self.data_slice_dropdown.getChoices() == 'USER-DEFINED FEATURE SET':
            self.feature_file_selected.entPath.config(state='normal')
        else:
            self.feature_file_selected.entPath.config(state='disabled')

    def add_to_listbox(self,
                       list_box: Listbox):
        value = self.value_entry_box.entry_get
        check_float(name='VALUE', value=value)
        list_box_content = [float(x) for x in list_box.get(0, END)]
        if float(value) not in list_box_content:
            list_box.insert(0, value)

    def remove_from_listbox(self,
                       list_box: Listbox):
        selection = list_box.curselection()
        if selection:
            list_box.delete(selection[0])




_ = UnsupervisedGUI(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini')


