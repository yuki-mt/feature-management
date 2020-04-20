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
df = manager.build_all()
```

## when feature code changes
```
df = YourFeature().get_features(update=True)

# or

manager.update_all()
df = YourFeature().get_features()
```

## reset DAG
```
from example_feat import gs
manager = FeatureManager(gs)
df = manager.build_all(overwrite=True)
```
