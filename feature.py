import pandas as pd
from abc import ABCMeta, abstractmethod
import os
import pickle
from dill.source import getsource
from typing import List, Dict
import subprocess
import re


class Feature(metaclass=ABCMeta):
    data_dir = './feat'
    class_dir = os.path.join(data_dir, 'py')
    dvc_dir = os.path.join(data_dir, 'dvc')

    # Apply Singleton pattern
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Feature, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.name = self.__class__.__name__
        self.df = pd.DataFrame()

    def __get_dependency(self, source: str) -> List[str]:
        return re.findall(r' +([^ =]+?)\(\)\.get_features\(', source)

    def __save_source(self, source: str) -> str:
        path = os.path.join(self.class_dir, self.name + '.py')
        with open(path, 'w') as f:
            f.write(source)
        return path

    def __output_path(self, postfix: str, name: str = '') -> str:
        postfix = '_' + postfix if postfix else ''
        name = name or self.name
        return os.path.join(self.data_dir, f'{name}{postfix}.pkl')

    def __dvc_path(self, postfix: str, name: str = '') -> str:
        postfix = '_' + postfix if postfix else ''
        name = name or self.name
        return os.path.join(self.dvc_dir, f'{name}{postfix}.pkl.dvc')

    def __save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.df, f)

    def __load(self, path: str):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.df = pickle.load(f)

    def get_features(self, postfix: str = '', update: bool = False) -> pd.DataFrame:
        if update:
            source = getsource(self.__class__)
            self.__save_source(source)
            command = f'dvc repro {self.__dvc_path(postfix)}'
            subprocess.run(command, shell=True)
        self.__load(self.__output_path(postfix))
        return self.df

    def build(self, all_feats: Dict[str, "Feature"], postfix: str, filepath: str, overwrite: bool = False):
        my_output_path = self.__output_path(postfix)
        if not overwrite and os.path.exists(self.__dvc_path(postfix)):
            return
        output_opt = '-o ' + my_output_path
        dvc_output_opt = '-f ' + self.__dvc_path(postfix)
        source = getsource(self.__class__)
        source_path = self.__save_source(source)
        dependencies = self.__get_dependency(source)
        dep_option_list = ['-d ' + source_path]
        for d in dependencies:
            all_feats[d].build(all_feats, postfix, filepath)
            dep_option_list.append('-d ' + self.__output_path(postfix, d))
        dep_option = ' '.join(dep_option_list)
        postfix_opt = f'--postfix {postfix}' if postfix else ''
        py_command = f'python {filepath} {self.name} {postfix_opt}'
        command = ' '.join(['dvc run', dep_option, output_opt, dvc_output_opt, py_command])
        print(f'run: {command}')
        subprocess.run(command, shell=True)

    def run_and_save(self, postfix: str):
        self.create_features(postfix)
        self.__save(self.__output_path(postfix))

    @abstractmethod
    def create_features(self, postfix: str):
        raise NotImplementedError
