import inspect
import pandas as pd
from feature import Feature
import os
import subprocess
import shutil


class FeatureManager:
    def __init__(self, namespace: dict):
        self.feature_dict = {}
        dirs = set()
        self.dvc_dirs = set()
        for k, v in namespace.items():
            if inspect.isclass(v) \
                    and issubclass(v, Feature) \
                    and not inspect.isabstract(v):
                instance = v()
                self.feature_dict[k] = instance
                dirs.add(instance.data_dir)
                dirs.add(instance.class_dir)
                dirs.add(instance.dvc_dir)
                self.dvc_dirs.add(instance.dvc_dir)
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        self.feature_path = namespace['__file__']

    def build_all(self, overwrite: bool = False):
        if overwrite:
            for d in self.dvc_dirs:
                shutil.rmtree(d)
                os.makedirs(d)
        for v in self.feature_dict.values():
            v.build(self.feature_dict, self.feature_path, overwrite=False)

    def update_all(self) -> pd.DataFrame:
        subprocess.run('dvc repro -P', shell=True)

def main_command():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("class_name", type=str)
    args = parser.parse_args()
    return f'{args.class_name}().run_and_save()'
