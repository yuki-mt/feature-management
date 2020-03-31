from typing import List
import inspect
import pandas as pd
from feature import Feature


class FeatureManager:
    def __init__(self, namespace, postfix: str):
        self.postfix = postfix
        self.feature_dict = {}
        for k, v in namespace.items():
            if inspect.isclass(v) \
                    and issubclass(v, Feature) \
                    and not inspect.isabstract(v):
                self.feature_dict[k] = v()
        self.feature_path = namespace['__file__']

    def get_all_names(self) -> List[str]:
        return list(self.feature_dict.keys())

    def build(self, feats: List[str], overwrite=False):
        for f in feats:
            self.feature_dict[f].build(self.feature_dict,
                                       self.postfix,
                                       self.feature_path)

    def get_features(self, feats: List[str], update: bool = False) -> pd.DataFrame:
        dfs = []
        for f in feats:
            dfs.append(self.feature_dict[f].get_features(self.postfix, update))
        return pd.concat(dfs, axis=1)


def main_command():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("class_name", type=str)
    parser.add_argument("--postfix", type=str, default='')
    args = parser.parse_args()
    return f'{args.class_name}().run_and_save("{args.postfix}")'
