from typing import List
import inspect
import pandas as pd
from feature import Feature


class FeatureManager:
    def __init__(self, namespace, postfix):
        self.features = []
        self.postfix = postfix
        for k, v in namespace.items():
            if inspect.isclass(v) and issubclass(v, Feature) and not inspect.isabstract(v):
                self.features.append(v())

    def get_all_names(self) -> List[str]:
        return [f.name for f in self.features]

    def get_features(self, feats: List[str],
                     overwrite: bool = False) -> pd.DataFrame:
        feat_set = set(feats)
        dfs = []
        for f in self.features:
            if f.name in feat_set:
                dfs.append(f.run(self.postfix, overwrite))
        return pd.concat(dfs, axis=1)
