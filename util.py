import inspect
from feature import Feature
import os
import subprocess
import shutil
import fire


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

    def build(self, overwrite: bool = False):
        if overwrite:
            for d in self.dvc_dirs:
                shutil.rmtree(d)
                os.makedirs(d)
        for v in self.feature_dict.values():
            v.build(self.feature_dict, self.feature_path)

    def update(self, feat: str):
        feature = self.feature_dict[feat]
        feature.update_source(self.feature_dict)
        feature.update_source(self.feature_dict)
        subprocess.run(f'dvc repro {feature.dvc_path}', shell=True)

    def run(self, feat: str):
        feature = self.feature_dict[feat]
        feature.run_and_save()


def main_command(namespace: dict):
    fire.Fire(FeatureManager(namespace))
