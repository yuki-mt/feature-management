from feature import Feature
from util import FeatureManager
import pandas as pd
import os


class Base(Feature):
    is_saved = False

    def create_features(self, postfix: str, overwrite: bool):
        if postfix == 'train':
            self.df = pd.DataFrame([[123, 2, 0], [345, 4, 1], [567, 6, 0]],
                                   columns=['col_1', 'col_2', 'label'])
        if postfix == 'test':
            self.df = pd.DataFrame([[987, 7], [543, 3], [321, 2]],
                                   columns=['col_1', 'col_2'])


class Sample(Feature):
    def create_features(self, postfix: str, overwrite: bool):
        df = Base().run(postfix, overwrite)
        self.df['sample_1'] = df.col_1.apply(lambda x: int(str(x)[0]))
        self.df['sample_2'] = df.col_1.apply(lambda x: int(str(x)[1]))


class Removed(Feature):
    def create_features(self, postfix: str, overwrite: bool):
        df = Base().run(postfix, overwrite)
        self.df = df.drop('col_2', axis=1)


if __name__ == '__main__':
    gs = globals()
    os.makedirs(Feature.dir_name, exist_ok=True)
    for postfix in ['train', 'test']:
        manager = FeatureManager(gs, postfix)
        names = manager.get_all_names()
        names.remove('Base')
        df = manager.get_features(names)
        print(postfix)
        print(df)
        print('====================')
    """
    Output is like below:


    train
       sample_1  sample_2  col_1  label
    0         1         2    123      0
    1         3         4    345      1
    2         5         6    567      0
    ====================
    test
       sample_1  sample_2  col_1
    0         9         8    987
    1         5         4    543
    2         3         2    321
    ====================
    """
