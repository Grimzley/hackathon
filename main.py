import pandas as pd
import numpy as np
import re
import random
import collections
import matplotlib.pyplot as plt

LEGAL_CHARACTERS_NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DIFF_SEP = ','
DEBUG = True


def diff_check(input_string) -> list:
    if len(input_string) < 2:
        return [0, 0, 0, 0]
    ret_val = []
    removals_str = ''
    times_removed_str = ''
    additions_str = ''
    times_added_str = ''
    parsing_removals = True
    parsing_times_removed = False
    parsing_additions = False
    # Parse out only the number of changes in the diff
    start_of_diff = 0
    for i in input_string:
        if i == '@':
            break
        start_of_diff += 1
    end_of_diff = start_of_diff + 2
    # Check for start of diff
    for i in range((start_of_diff + 2), len(input_string)):
        if input_string[i] == '@':
            break
        end_of_diff += 1
    result_string = ''
    # Check for the end of the diff
    for i in range(start_of_diff + 2, end_of_diff):
        result_string = result_string + input_string[i]
    # if DEBUG: print(f'PARSED DIFF: {result_string}')
    # Get the number of removals and additions to the diff
    for i in result_string:
        if i not in LEGAL_CHARACTERS_NUMBERS:  # Skip characters not allowed to be in our diff count
            if i == DIFF_SEP:  # Characters following are something new
                if parsing_removals:
                    parsing_removals = False
                    parsing_times_removed = True
                else:
                    parsing_additions = False
            elif i == '+':
                if parsing_removals:
                    times_removed_str = '0'
                    parsing_removals = False
                else:
                    parsing_times_removed = False
                parsing_additions = True
        else:  # Use characters allowed in our diff count
            if parsing_removals:
                removals_str = removals_str + i
            elif parsing_times_removed:
                times_removed_str = times_removed_str + i
            elif parsing_additions:
                additions_str = additions_str + i
            else:  # Times added
                times_added_str = times_added_str + i
    # Cast to integers

    removals = int(removals_str)
    ret_val.append(removals)
    times_removed = int(times_removed_str)
    ret_val.append(times_removed)
    additions = int(additions_str)
    ret_val.append(additions)
    if parsing_additions:
        times_added = 0
    else:
        times_added = int(times_added_str)
    ret_val.append(times_added)
    return ret_val


def weighted_word_frequency(data):
    dictionary = []
    body = data['body']
    
    # clean data
    for index, message in enumerate(body):
        message = message.lower()
        message = re.sub(r'[^a-z0-9]', ' ',message)
        message = message.split()
        body[index] = message
    
    # get diff of all entries
    diff = []
    diff_count = 0
    for i in range(data.shape[0]):
        # print(df.loc[i]["diff"])
        curr_diff = diff_check(input_string=data.loc[i]["diff"])
        diff.append(curr_diff[0] + curr_diff[2])
        diff_count += curr_diff[0] + curr_diff[2]
    diff.sort()
    avg_diff = diff_count / data.shape[0]  
    
    # add words to dictionary
    for message in body:
        for word in message:
            dictionary.append(word)
    dictionary = list(set(dictionary)) # remove duplicate words
    
    # count the number of occurences of each word in each body message and add weights
    word_count = {word: [0] * len(body) for word in dictionary} # initialize word counts to 0
    weighted_word_count = {word: [0] * len(body) for word in dictionary} # initialize weight counts to 0
    for index, message in enumerate(body):
        for word in message:
            word_count[word][index] += 1
            weighted_word_count[word][index] += diff[index]
    
    weighted_word_count = {word: sum(weighted_word_count[word]) / sum(word_count[word]) for word in dictionary}
    diff.sort()
    counter = collections.Counter(diff)
    print(list(counter.keys()))
    print(list(counter.values()))
    plt.scatter(list(counter.keys())[7:-2], list(counter.values())[7:-2])
    plt.title('Diffs w/ Outliers removed')
    plt.xlabel('Num of changes in diff')
    plt.ylabel('Frequency')
    plt.show()
    return weighted_word_count


def main() -> None:
    df = pd.read_pickle('data_clean.pkl')
    shape = df.shape
    df['index'] = range(shape[0])
    df = df.set_index('index')
    df = df.drop('pullrequest_id', 1)
    df = df.drop('repo_id', 1)
    df = df.drop('repo_full_name', 1)
    
    print(df.head())
    code_line = random.randint(0, shape[0])  # change this
    # code_line = 511
    if DEBUG: print(f'ORIGINAL HASH : \n {df.loc[code_line]["original_commit_hash"]}')
    if DEBUG: print(f'POST MERGE HASH : \n {df.loc[code_line]["post_merge_hash"]}')
    if DEBUG: print(f'Body : \n {df.loc[code_line]["body"]}')
    if DEBUG: print(f'File Path : \n {df.loc[code_line]["file_path"]}')
    if DEBUG: print(f'Code : \n {df.loc[code_line]["code"]}')
    if DEBUG: print(f'Diff : \n {df.loc[code_line]["diff"]}')
    
    weighted_word_count = weighted_word_frequency(df)


if __name__ == '__main__':
    main()
