import time
import numpy as np
import pandas as pd
from scipy.stats import kurtosis
from utils import unique_count, map_period, total_duration_percentage, map_button

mistake_touch = ['MediaPlayPause', 'AudioVolumeUp', 'Cancel', 'Pause', 'AudioVolumeMute', 'ContextMenu',
                 'MediaTrackPrevious', 'AudioVolumeDown', 'ModeChange', 'MediaTrackNext', 'Dead', 'Process', 'Clear',
                 'Alt', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15']
agg_dict = {'event_id': ['count'],
            'down_time': ['sum', 'mean', 'median', 'std', 'max', 'min', 'skew', kurtosis, 'count'],
            'up_time': ['sum', 'mean', 'median', 'std', 'max', 'min', 'skew', kurtosis, 'count'],
            'action_time': ['sum', 'mean', 'median', 'std', 'max', 'min', 'skew', kurtosis, 'count'],
            'activity': [unique_count],
            'down_event': [unique_count],
            'up_event': [unique_count],
            'text_change': [unique_count],
            'cursor_position': [unique_count],
            'word_count': ['sum', 'mean', 'median', 'std', 'max', 'min', 'skew', kurtosis, 'count'],
            'period_5_min': [unique_count],
            'period_10_min': [unique_count],
            'pressed_button_type': [unique_count],
            'is_mistake_touch': ['sum', 'mean', 'median', 'std', 'max', 'min', 'skew', kurtosis, 'count']
            }

file_path = 'data/train_logs.csv'

if __name__ == '__main__':
    df = pd.read_csv(file_path, nrows=10)

    # add new columns
    # add time gap
    print('checkpoint1')
    df = map_period(df, 'down_time', [5, 10])

    # add pressed button type
    print('checkpoint2')
    df['pressed_button_type'] = df['down_event'].apply(map_button)

    # add is_mistake_touch
    print('checkpoint3')
    df['is_mistake_touch'] = df['down_event'].apply(lambda x: 1 if x in mistake_touch else 0)

    # change column value
    print('checkpoint4')
    df['activity'] = df['activity'].apply(lambda x: 'Move' if x.startswith('Move') else x)

    # group by id
    print('checkpoint5')
    group_by_id_df = df.groupby(['id']).agg(agg_dict)

    # group by id and other columns
    print('checkpoint6')
    for column in df.columns:
        print(column)
        if column != 'id':
            agg_dict_ = agg_dict.copy()
            del agg_dict_[column]
            group_df = df.groupby(['id', column]).agg(agg_dict_)
        time.sleep(1)


    # add information
    # add action style

    # add time period 5mins 10mins

    # print(grouped_df.head(10))
