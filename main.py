import pandas as pd
import numpy as np
import re


def main() -> None:
    df = pd.read_pickle('data_clean.pkl')
    shape = df.shape
    #print(shape)
    df['index'] = range(shape[0])
    df = df.set_index('index')
    df = df.drop('pullrequest_id', 1)
    df = df.drop('repo_id', 1)
    df = df.drop('repo_full_name', 1)
    '''
    print(df.head())
    code_line = 72  # change this
    print(f'ORIGINAL HASH : \n {df.loc[code_line]["original_commit_hash"]}')
    print(f'POST MERGE HASH : \n {df.loc[code_line]["post_merge_hash"]}')
    print(f'Body : \n {df.loc[code_line]["body"]}')
    print(f'File Path : \n {df.loc[code_line]["file_path"]}')
    print(f'Code : \n {df.loc[code_line]["code"]}')
    print(f'Diff : \n {df.loc[code_line]["diff"]}')
    '''
    word_count = frequency(df)

def frequency(data):
    dictionary = []
    body = data['body']
    
    # clean data
    for index, message in enumerate(body):
        message = message.lower()
        message = re.sub(r'[^a-zA-Z0-9]', ' ',message)
        message = message.split()
        body[index] = message
    
    # add words to dictionary
    for message in body:
        for word in message:
            dictionary.append(word)
    dictionary = list(set(dictionary)) # remove duplicate words
    # count the number of occurences of each word in each body message
    word_count = {word: [0] * len(body) for word in dictionary} # initialize word counts to 0
    for index, message in enumerate(body):
        for word in message:
            word_count[word][index] += 1
    return word_count

if __name__ == '__main__':
    main()
