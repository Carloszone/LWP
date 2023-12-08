import numpy as pd
import pandas as pd

feature_file = 'data/train_logs.csv'
cats = ['activity', 'down_event', 'up_event', 'text_update']
mouse_operation = ['Leftclick', 'Middleclick', 'Rightclick', 'Unknownclick']
feature_key_operation = ['F10', 'Home', 'CapsLock', 'Escape', 'NumLock', 'ArrowLeft', 'Insert', 'MediaPlayPause',
                         'Space', 'ArrowUp', 'PageDown', 'ArrowDown', 'AltGraph', 'ArrowRight', 'AudioVolumeUp',
                         'Cancel', 'Pause', 'Shift', 'AudioVolumeMute', 'ContextMenu', 'MediaTrackPrevious',
                         'Backspace', 'ScrollLock',  'AudioVolumeDown', 'ModeChange', 'MediaTrackNext', 'Control',
                         'Enter', 'Delete', 'Dead', 'Process', 'PageUp', 'Clear', 'Alt', 'Meta', 'Tab', 'End']
mistake_touch = ['MediaPlayPause', 'F10', 'AudioVolumeUp', 'Cancel', 'Pause', 'AudioVolumeMute', 'ContextMenu',
                 'MediaTrackPrevious', 'AudioVolumeDown', 'ModeChange', 'MediaTrackNext', 'Dead', 'Process', 'Clear',
                 'Alt', 'F12']

df = pd.read_csv(feature_file)
print(df['activity'].value_counts())

g = []
for name in ['Nonproduction', 'Input', 'Remove/Cut', 'Paste', 'Replace', 'Move From']:
    g1 = df[df['activity'].str.startswith(name)]['up_event'].unique().tolist()
    g2 = df[df['activity'].str.startswith(name)]['down_event'].unique().tolist()
    g = g+g1+g2
print('**********************')
print(set(g))


# {'Unidentified', 'w', 'q', 'OS', '!', 's', 'j', '\x80', ',',
#   'Å\x9f',  'Â´',  '=', ']', 'f',  ';', 'F3', 'u',
#  'Ë\x86', 'm', 'V', ')', '.', '*', '<',  '#', 'C', '{',   '\x9b',  'c',
#  'ä', '\x97', '^',  '/', '~', 'e',  '`', '[',
#  '(',  'l', 'x', '¿', 'n',  'I', 'F12',
#   'i', '+', 'F',  '%', 'd', '\x96', '&', 't', '5',
#  'F1',  '_', 'b', '¡', 'v', 'z', 'A', '-', 'Ä±', 'p',  'â\x80\x93', 'a', '$', 'y',
#   '\\', '2', 'F15', 'k',   'M', '@', 'F11', 'o', '0', "'", '1',  '"', 'F6', 'T', 'h',
#  'r', '}', '>', ':', 'g', 'S', '?',   '|'}

