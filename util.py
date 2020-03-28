from typing import List
import inspect
import pandas as pd
from feature import Feature


class FeatureManager:
    def __init__(self, namespace, postfix: str, is_graph: bool = True):
        self.postfix = postfix
        self.is_graph = is_graph
        self.features = []
        for v in namespace.values():
            if inspect.isclass(v) \
                    and issubclass(v, Feature) \
                    and not inspect.isabstract(v):
                self.features.append(v())

    def get_all_names(self) -> List[str]:
        return [f.name for f in self.features]

    def get_features(self, feats: List[str],
                     overwrite: bool = False) -> pd.DataFrame:
        if self.is_graph and overwrite:
            from pycallgraph import PyCallGraph, Config
            config = Config(groups=False,
                            output='graphviz',
                            include=["*.run", "*.create_features"],
                            exclude=[])
            config.convert_filter_args()
            with PyCallGraph(config=config):
                return self.__get_features(feats, overwrite)
        else:
            return self.__get_features(feats, overwrite)

    def __get_features(self, feats: List[str],
                       overwrite: bool = False) -> pd.DataFrame:
        feat_set = set(feats)
        dfs = []
        for f in self.features:
            if f.name in feat_set:
                dfs.append(f.run(self.postfix, overwrite))
        return pd.concat(dfs, axis=1)
