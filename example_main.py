from example_feat import gs
from util import FeatureManager


if __name__ == '__main__':
    manager = FeatureManager(gs)
    for postfix in ['train', 'test']:
        manager.build_all(postfix)
        names = manager.get_all_names()
        names.remove('Base')
        df = manager.get_features(names, postfix)
        print(postfix)
        print(df)
        print('====================')
    """
    Output is like below:


    train
       sample_1  sample_2  col_1  label
    0         1         2    123      0
    1         3         4    345      1
    2         5         6    567      0
    ====================
    test
       sample_1  sample_2  col_1
    0         9         8    987
    1         5         4    543
    2         3         2    321
    ====================
    """
