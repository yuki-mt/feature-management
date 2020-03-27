import pandas as pd
import time
from abc import ABCMeta, abstractmethod
from os import path
from contextlib import contextmanager
from typing import Dict


@contextmanager
def timer(name):
    t0 = time.time()
    print(f'[{name}] start')
    yield
    print(f'[{name}] done in {time.time() - t0:.0f} s')


class Feature(metaclass=ABCMeta):
    dir_name = '.'
    memo: Dict[str, str] = {}
    train_path_fmt = path.join(dir_name, '{}_train.pkl')
    test_path_fmt = path.join(dir_name, '{}_train.pkl')

    def __init__(self):
        self.name = self.__class__.__name__
        self.train = pd.DataFrame()
        self.test = pd.DataFrame()
        self.train_path = Feature.train_path_fmt.format(self.name)
        self.test_path = Feature.test_path_fmt.format(self.name)

    def run(self, overwrite: bool = False):
        with timer(self.name):
            self.create_features()
            Feature.memo[self.name] = self.description

            if path.exists(self.train_path)and path.exists(self.test_path) and not overwrite:
                print(self.name, 'was skipped')
            else:
                self.train.to_pickle(self.train_path)
                self.test.to_pickle(self.test_path)

    @abstractmethod
    def create_features(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @classmethod
    def get_memo_df(cls):
        data = sorted(cls.memo.items(), key=lambda x: x[0])
        return pd.DataFrame(data, columns=['name', 'description'])
