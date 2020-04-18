from example_feat import gs
from util import FeatureManager


if __name__ == '__main__':
    manager = FeatureManager(gs)
    manager.build_all()
    names = manager.get_all_names()
    names.remove('Base')
    df = manager.get_features(names)
    print(df)
    print('====================')
    """
    Output is like below:


       sample_1  sample_2  col_1  label
    0         1         2    123      0
    1         3         4    345      1
    2         5         6    567      0
    ====================
    """
