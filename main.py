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
    code_line = 72  # change this
    print(f'ORIGINAL HASH : \n {df.loc[code_line]["original_commit_hash"]}')
    print(f'POST MERGE HASH : \n {df.loc[code_line]["post_merge_hash"]}')
    print(f'Body : \n {df.loc[code_line]["body"]}')
    print(f'File Path : \n {df.loc[code_line]["file_path"]}')
    print(f'Code : \n {df.loc[code_line]["code"]}')
    print(f'Diff : \n {df.loc[code_line]["diff"]}')


if __name__ == '__main__':
    main()
