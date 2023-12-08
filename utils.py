import numpy as np
import pandas as pd
import scipy

mouse_operation = ['Leftclick', 'Middleclick', 'Rightclick', 'Unknownclick']
feature_key_operation = ['Home', 'CapsLock', 'Escape', 'NumLock', 'ArrowLeft', 'Insert', 'MediaPlayPause',
                         'ArrowUp', 'PageDown', 'ArrowDown', 'AltGraph', 'ArrowRight', 'AudioVolumeUp',
                         'Cancel', 'Pause', 'Shift', 'AudioVolumeMute', 'ContextMenu', 'MediaTrackPrevious',
                         'ScrollLock', 'AudioVolumeDown', 'ModeChange', 'MediaTrackNext', 'Control',
                         'Enter', 'Delete', 'Dead', 'Process', 'PageUp', 'Clear', 'Alt', 'Meta', 'Tab', 'End']


def map_button(operation):
    if operation in mouse_operation:
        return 'mouse'
    elif operation in feature_key_operation:
        return 'feature_key'
    elif (operation == 'p') or (operation == 'space') or (operation == 'backspace') or (operation == 'enter'):
        return 'input'
    elif pd.isnull(operation) or operation == '' or operation == np.NAN:
        return 'empty'
    else:
        return 'other'


def map_period(df, column, gaps):
    df['time_in_min'] = df[column] / (1000 * 60)

    for gap in gaps:
        df[f'period_{gap}_min'] = np.ceil(df['time_in_min'] / gap)

    df = df.drop(columns=['time_in_min'])
    return df


def total_duration_percentage(series):
    return series.sum() / series.sum().sum()


# data generation
def unique_count(series: pd.Series) -> int:
    return series.nunique()


def is_nan_check(df):
    check = df.isnull().sum().sum()
    columns_with_nan = df.columns[df.isna().any()].tolist()
    if check == 0:
        print('No missing value')
    else:
        print(f'There are {check} missing values')
        print("Columns with NaN values:", columns_with_nan)

def rmse(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

