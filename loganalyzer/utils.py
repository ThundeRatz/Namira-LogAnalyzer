import json
import pandas as pd

def write_json(save_path, dictionary):
    with open(save_path, 'w') as outfile:
        json.dump(dictionary, outfile)

def write_csv(save_path, list_of_lines, header=None):
    dataframe = pd.DataFrame(list_of_lines)
    if header is None:
        dataframe.to_csv(save_path, index=False, header=False)
    else:
        dataframe.to_csv(save_path, index=False, header=header)