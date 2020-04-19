import pandas as pd
from abc import ABCMeta, abstractmethod
import os
import pickle
from dill.source import getsource
from typing import List, Dict
import subprocess
import re


"""
run instances of this class through FeatureManager
"""
class Feature(metaclass=ABCMeta):
    data_dir = './feat'
    class_dir = os.path.join(data_dir, '.py')
    dvc_dir = os.path.join(data_dir, '.dvc')

    # Apply Singleton pattern
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Feature, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_dependencies: List[str] = []):
        self.name = self.__class__.__name__
        self.df = pd.DataFrame()
        self.file_dependencies = file_dependencies
        self.dvc_path = os.path.join(self.dvc_dir, f'{self.name}.pkl.dvc')

    def __get_dependency(self, source: str) -> List[str]:
        return re.findall(r' +([^ =]+?)\(\)\.get_features\(', source)

    def __save_source(self, source: str) -> str:
        path = os.path.join(self.class_dir, self.name + '.py')
        with open(path, 'w') as f:
            f.write(source)
        return path

    def __output_path(self, name: str = '') -> str:
        name = name or self.name
        return os.path.join(self.data_dir, f'{name}.pkl')

    def __save(self):
        with open(self.__output_path(), 'wb') as f:
            pickle.dump(self.df, f)

    def __load(self):
        path = self.__output_path()
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.df = pickle.load(f)

    def get_features(self, update: bool = False) -> pd.DataFrame:
        if update:
            source = getsource(self.__class__)
            self.__save_source(source)
            command = f'dvc repro {self.dvc_path}'
            subprocess.run(command, shell=True)
        self.__load()
        return self.df

    def build(self, all_feats: Dict[str, "Feature"], filepath: str, overwrite: bool = False):
        if not overwrite and os.path.exists(self.dvc_path):
            return
        output_opt = '-o ' + self.__output_path()
        dvc_output_opt = '-f ' + self.dvc_path
        source = getsource(self.__class__)
        source_path = self.__save_source(source)
        dependencies = self.__get_dependency(source)
        dep_option_list = ['-d ' + d for d in (self.file_dependencies + [source_path])]
        for d in dependencies:
            all_feats[d].build(all_feats, filepath)
            dep_option_list.append('-d ' + self.__output_path(d))
        dep_option = ' '.join(dep_option_list)
        py_command = f'python {filepath} {self.name}'
        command = ' '.join(['dvc run', dep_option, output_opt, dvc_output_opt, py_command])
        subprocess.run(command, shell=True)

    def run_and_save(self):
        self.create_features()
        self.__save()

    @abstractmethod
    def create_features(self):
        """
        assign a new feature to self.df
        """
        raise NotImplementedError
