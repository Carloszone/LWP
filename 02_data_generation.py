import os
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from utils import unique_count, map_period, total_duration_percentage, map_button, is_nan_check

mistake_touch = ['MediaPlayPause', 'AudioVolumeUp', 'Cancel', 'Pause', 'AudioVolumeMute', 'ContextMenu',
                 'MediaTrackPrevious', 'AudioVolumeDown', 'ModeChange', 'MediaTrackNext', 'Dead', 'Process', 'Clear']
mouse_operation = ['Leftclick', 'Middleclick', 'Rightclick', 'Unknownclick']
feature_key_operation = ['Home', 'CapsLock', 'Escape', 'NumLock', 'ArrowLeft', 'Insert', 'MediaPlayPause',
                         'ArrowUp', 'PageDown', 'ArrowDown', 'AltGraph', 'ArrowRight', 'AudioVolumeUp',
                         'Cancel', 'Pause', 'Shift', 'AudioVolumeMute', 'ContextMenu', 'MediaTrackPrevious',
                         'ScrollLock', 'AudioVolumeDown', 'ModeChange', 'MediaTrackNext', 'Control',
                         'Enter', 'Delete', 'Dead', 'Process', 'PageUp', 'Clear', 'Alt', 'Meta', 'Tab', 'End']
F_keys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15']
signs = ['!', ',', '=', ']', ';', ')', '.', '*', '<', '#', '{', '^', '/', '~', '`', '[', '(', '¿', '+', '%', '&', '_',
         '-', '$', '\\', '@', "'", '"', '}', '>', ':', '?', '|']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
agg_dict = {'down_time': ['sum', 'mean', 'median', 'max', 'min', 'count'],
            'up_time': ['sum', 'mean', 'median', 'max', 'min', 'count'],
            'action_time': ['sum', 'mean', 'median', 'max', 'min', 'count'],
            'activity': [unique_count],
            'down_event': [unique_count],
            'up_event': [unique_count],
            'text_change': [unique_count],
            'cursor_position': [unique_count, 'max'],
            'word_count': ['sum', 'mean', 'median', 'max', 'min', 'count'],
            'period_5_min': [unique_count],
            'period_10_min': [unique_count],
            'pressed_button_type': [unique_count],
            'is_mistake_touch': ['sum', 'mean', 'median', 'max', 'min', 'count']
            }


def data_generation(paths):
    for path in tqdm(paths):
        df = pd.read_csv(path)

        # add new columns
        # add time gap
        df = map_period(df, 'down_time', [5, 10])

        # add pressed button type
        df['pressed_button_type'] = df['down_event'].apply(map_button)

        # add is_mistake_touch
        df['is_mistake_touch'] = df['down_event'].apply(lambda x: 1 if x in mistake_touch + F_keys else 0)

        # add word_length
        # df['word_length'] = (df['cursor_position'] + 1e-10) / (df['word_count'] + 1e-10)

        # change column value
        df['activity'] = df['activity'].apply(lambda x: 'Move' if x.startswith('Move') else x)

        for column in ['down_event', 'up_event']:
            conditions = [df[column].isin(F_keys), df[column].isin(mouse_operation), df[column].isin(feature_key_operation),
                          df[column] == 'q', df[column].isin(signs), df[column].isin(numbers)]
            categories = ['F_keys', 'mouse', 'feature_key', 'input', 'signs', 'numbers']
            df[column] = np.select(conditions, categories, default='other')

        # group by id
        group_by_id_df = df.groupby(['id']).agg(agg_dict)
        group_by_id_df.columns = [f'{col[0]}_{col[1]}' for col in group_by_id_df.columns]
        group_by_id_df['word_length'] = group_by_id_df['cursor_position_max'] / group_by_id_df['word_count_max'] - 2
        merged_df = group_by_id_df.copy().reset_index()
        # is_nan_check(group_by_id_df)

        # group by id and other columns
        for column in df.columns:
            if column not in ['id', 'event_id', 'up_time', 'down_time', 'action_time', 'cursor_position', 'word_count']:
                agg_dict_ = agg_dict.copy()
                del agg_dict_[column]
                group_df = df.groupby(['id', column]).agg(agg_dict_)
                group_df.columns = [f'{col[0]}_{col[1]}' for col in group_df.columns]
                group_df['word_length'] = group_df['cursor_position_max'] / group_df['word_count_max'] - 2
                group_df = group_df.reset_index().pivot_table(index='id', columns=column, values=list(group_df.columns)[2:],
                                                              fill_value=0)
                group_df.columns = [f'{col[0]}_{col[1]}' for col in group_df.columns if col != 'id']
                merged_df = merged_df.merge(group_df, on='id', how='left', suffixes=('', f'_{column}'))
            time.sleep(1)

        # save file
        merged_df.to_csv(path.replace('train_logs', 'engineered_train_logs'), index=False)

if __name__ == '__main__':
    paths = []
    for dirname, _, filenames in os.walk('datasets'):
        for filename in filenames:
            paths.append(os.path.join(dirname, filename))

    data_generation(paths)

