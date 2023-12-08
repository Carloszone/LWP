# load packages
import pandas as pd
import os
from tqdm import tqdm


def split_data_set(df, k_fold):
    unique_ids = df['id'].unique().tolist()
    length = len(unique_ids) // k_fold
    new_file_paths = []

    print(f'start to split data into {k} fold')
    for i in tqdm(range(k_fold)):
        if i < k_fold-1:
            split_ids = unique_ids[i*length:(i+1)*length]
        else:
            split_ids = unique_ids[i*length:]
            sub_df = df[df['id'].isin(split_ids)]

            if not os.path.exists('datasets'):
                os.mkdir('datasets')

            new_file_path = os.path.join('datasets', f'{file}_{i}.{file_type}')
            sub_df.to_csv(new_file_path, index=False)
            new_file_paths.append(new_file_path)

    return new_file_paths

if __name__ == '__main__':
    # parameter setting
    original_folder = 'data'
    file = 'train_logs'
    file_type = 'csv'
    k = 10

    # read csv file
    path = os.path.join(original_folder, f'{file}.{file_type}')
    dataframe = pd.read_csv(path)

    # call function
    split_data_set(dataframe, k)

