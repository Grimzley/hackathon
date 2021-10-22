import pandas as pd
import numpy as np


def main() -> None:
    df = pd.read_pickle('data_clean.pkl')
    shape = df.shape
    print(shape)
    df['index'] = range(shape[0])
    df = df.set_index('index')
    df = df.drop('pullrequest_id', 1)
    df = df.drop('repo_id', 1)
    df = df.drop('repo_full_name', 1)
    print(df.head())


if __name__ == '__main__':
    main()
