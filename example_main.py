from example_feat import Final


if __name__ == '__main__':
    df = Final().get_features()
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
