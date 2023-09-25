import json
import pandas as pd

def split_list(list_, number):
    if list_ == [] or number < 1:
        return list_
    k, m = divmod(len(list_), number)
    return (list_[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(number))


def write_json(save_path, dictionary):
    with open(save_path, 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


def write_csv(save_path, list_of_lines, header=None):
    dataframe = pd.DataFrame(list_of_lines)
    if header is None:
        dataframe.to_csv(save_path, index=False, header=False)
    else:
        dataframe.to_csv(save_path, index=False, header=header)