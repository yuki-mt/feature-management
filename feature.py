import pandas as pd
from abc import ABCMeta, abstractmethod
import os
import pickle
from dill.source import getsource
from typing import List, Dict
import subprocess
import re
from copy import deepcopy


class Feature(metaclass=ABCMeta):
    data_dir: str

    # Apply Singleton pattern
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Feature, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_dependencies: List[str] = []):
        self.name = self.__class__.__name__
        self.df = pd.DataFrame()
        self.file_dependencies = file_dependencies
        self.class_dir = os.path.join(self.data_dir, '.pysource')
        self.dvc_dir = os.path.join(self.data_dir, '.dvcfiles')
        self.dvc_path = os.path.join(self.dvc_dir, f'{self.name}.pkl.dvc')

    def __get_dependency(self, source: str) -> List[str]:
        return re.findall(r' +([^ =]+?)\(\)\.get_features\(', source)

    def __save_source(self, source: str) -> str:
        path = os.path.join(self.class_dir, self.name + '.py')
        with open(path, 'w') as f:
            f.write(source)
        return path

    def output_path(self, name: str = '') -> str:
        name = name or self.name
        return os.path.join(self.data_dir, f'{name}.pkl')

    def __save(self):
        with open(self.output_path(), 'wb') as f:
            pickle.dump(self.df, f)

    def __load(self):
        path = self.output_path()
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.df = pickle.load(f)

    def update_source(self, all_feats: Dict[str, "Feature"]) -> None:
        """
        supposed to run this through FeatureManager
        """
        source = getsource(self.__class__)
        self.__save_source(source)
        dependencies = self.__get_dependency(source)
        for d in dependencies:
            all_feats[d].update_source(all_feats)

    def get_features(self) -> pd.DataFrame:
        self.__load()
        return deepcopy(self.df)

    def build(self, all_feats: Dict[str, "Feature"], filepath: str):
        """
        supposed to run this through FeatureManager
        """
        if os.path.exists(self.dvc_path):
            return
        output_opt = '-o ' + self.output_path()
        dvc_output_opt = '-f ' + self.dvc_path
        source = getsource(self.__class__)
        source_path = self.__save_source(source)
        dependencies = self.__get_dependency(source)
        dep_option_list = ['-d ' + d for d in (self.file_dependencies + [source_path])]
        for d in dependencies:
            all_feats[d].build(all_feats, filepath)
            dep_option_list.append('-d ' + self.output_path(d))
        dep_option = ' '.join(dep_option_list)
        py_command = f'python {filepath} run {self.name}'
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
