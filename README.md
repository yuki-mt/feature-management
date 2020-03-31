# Feature management

From: https://amalog.hateblo.jp/entry/kaggle-feature-management

## Run example
```
pip install -r requirements.txt
dvc init
python example_main.py
```

## when feature code changes
```
from example_feat import gs
manager = FeatureManager(gs, postfix)
names = manager.get_all_names()
df = manager.get_features(names, update=True)
```

## when dependency changes
```
from example_feat import gs
manager = FeatureManager(gs, postfix)
df = manager.build(['ChangedFeature'], overwrite=True)
```
