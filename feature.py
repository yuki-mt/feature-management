import pandas as pd
from abc import ABCMeta, abstractmethod
import os


class Feature(metaclass=ABCMeta):
    dir_name = './feat'
    is_saved = True

    # Apply Singleton pattern
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Feature, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.name = self.__class__.__name__
        self.df = pd.DataFrame()
        self.path_fmt = os.path.join(self.dir_name, self.name + '{}.pkl')

    def __save(self, path: str):
        if self.is_saved:
            self.df.to_pickle(path)

    def __load(self, path: str):
        if self.is_saved and os.path.exists(path):
            self.df = pd.read_pickle(path)

    def run(self, postfix: str, overwrite: bool) -> pd.DataFrame:
        path = self.path_fmt.format(f'_{postfix}' if postfix else '')
        self.__load(path)
        if overwrite or self.df.empty:
            self.create_features(postfix, overwrite)
            self.__save(path)
        return self.df

    @abstractmethod
    def create_features(self, postfix: str, overwrite: bool):
        raise NotImplementedError
