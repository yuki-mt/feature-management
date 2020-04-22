# Feature management

From: https://amalog.hateblo.jp/entry/kaggle-feature-management <br>
apply DVC

## Run example
```
pip install -r requirements.txt
dvc init
python example_feat.py build
python example_main.py
```

## intially build DVC DAG
```
python example_feat.py build
```

## when feature code changes
```
python example_feat.py update <feature_class_name>
```

## reset DAG
```
python example_feat.py build --overwrite=True
```

## Display DAG in Jupyter notebook
```
!sudo apt-get install -y graphviz

dvc_dir = Final().dvc_dir
dot_filename = 'dag.dot'
!cd {dvc_dir} && dvc pipeline show --dot Final.pkl.dvc > {dot_filename}
import pydotplus
from IPython.display import Image
import os

png_path = 'dag.png'
dot_path = os.path.join(dvc_dir, dot_filename)
graph = pydotplus.graphviz.graph_from_dot_file(dot_path)
graph.write_png(png_path)
Image(graph.create_png())
!rm {png_path} {dot_path}
```
