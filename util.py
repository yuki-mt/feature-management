from typing import List
import inspect
import pandas as pd
from feature import Feature


def get_features(namespace):
    for k, v in namespace.items():
        if inspect.isclass(v) and issubclass(v, Feature) and not inspect.isabstract(v):
            yield k, v


def generate_features(namespace, overwrite: bool = False):
    for k, v in get_features(namespace):
        v().run(overwrite)


def load_datasets(feats: List[str]):
    dfs = [pd.read_pickle(f'{Feature.dir_name}/{f}_train.pkl') for f in feats]
    X_train = pd.concat(dfs, axis=1)
    dfs = [pd.read_pickle(f'{Feature.dir_name}/{f}_test.pkl') for f in feats]
    X_test = pd.concat(dfs, axis=1)
    return X_train, X_test
