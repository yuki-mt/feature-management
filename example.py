from feature import Feature
from util import generate_features, load_datasets, get_features
import pandas as pd
import os


class Sample(Feature):
    def create_features(self):
        self.train['sample_1'] = df.col_1.apply(lambda x: int(str(x)[0]))
        self.train['sample_2'] = df.col_1.apply(lambda x: int(str(x)[1]))

    @property
    def description(self):
        return '1st & 2nd digit of col_1'


if __name__ == '__main__':
    df = pd.DataFrame([[123, 2], [345, 4], [567, 6]],
                      columns=['col_1', 'col_2'])

    gs = globals()
    os.makedirs(Feature.dir_name, exist_ok=True)
    generate_features(gs)

    feats = [k for k, _ in get_features(gs)]
    X_train, _ = load_datasets(feats)
    all_df = pd.concat([df, X_train], axis=1)

    print(all_df)
    print('==============')
    print(Feature.get_memo_df())
