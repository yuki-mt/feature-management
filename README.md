# Feature management

From: https://amalog.hateblo.jp/entry/kaggle-feature-management <br>
apply DVC

## Run example
```
pip install -r requirements.txt
dvc init
python example_main.py
```

## intially build DVC DAG
```
from example_feat import gs
manager = FeatureManager(gs)
df = manager.build_all(postfix)
```

## when feature code changes
```
from example_feat import gs
manager = FeatureManager(gs)
names = manager.get_all_names()

df = manager.get_features(names, postfix, update=True)

# or

manager.update_all()
df = manager.get_features(names, postfix)
```

## when dependency changes
```
from example_feat import gs
manager = FeatureManager(gs)
df = manager.build(['ChangedFeature'], postfix, overwrite=True)
```
