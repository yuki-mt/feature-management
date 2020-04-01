from feature import Feature
from util import main_command
import pandas as pd


class Base(Feature):
    def __init__(self):
        super().__init__(
            file_dependencies=['./dataset/train.csv', './dataset/test.csv'])

    def create_features(self, postfix: str):
        if postfix == 'train':
            self.df = pd.read_csv(self.file_dependencies[0],
                                  names=['col_1', 'col_2', 'label'])
        if postfix == 'test':
            self.df = pd.read_csv(self.file_dependencies[1],
                                  names=['col_1', 'col_2'])


class Sample(Feature):
    def create_features(self, postfix: str):
        df = Base().get_features(postfix)
        self.df['sample_1'] = df.col_1.apply(lambda x: int(str(x)[0]))
        self.df['sample_2'] = df.col_1.apply(lambda x: int(str(x)[1]))


class Removed(Feature):
    def create_features(self, postfix: str):
        df = Base().get_features(postfix)
        self.df = df.drop('col_2', axis=1)


gs = globals()


if __name__ == '__main__':
    exec(main_command())