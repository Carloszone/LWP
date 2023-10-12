import numpy as pd
import pandas as pd

feature_file = 'data/train_logs.csv'
cats = ['activity', 'down_event', 'up_event', 'text_update']
mouse_operation = ['Leftclick', '']

df = pd.read_csv(feature_file)
print(df['activity'].value_counts())

g = []
for name in ['Nonproduction', 'Input', 'Remove/Cut', 'Paste', 'Replace', 'Move From']:
    g1 = df[df['activity'].str.startswith(name)]['up_event'].unique().tolist()
    g2 = df[df['activity'].str.startswith(name)]['down_event'].unique().tolist()
    g = g+g1+g2
print('**********************')
print(set(g))


{'Middleclick', 'F10', 'Unidentified', 'w', 'q', 'OS', '!', 's', 'Home', 'j', '\x80', ',', 'CapsLock', 'Escape',
 'NumLock', 'Å\x9f', 'ArrowLeft', 'Â´', 'Insert', '=', 'Unknownclick', ']', 'f', 'Leftclick', ';', 'F3', 'u', 'Meta',
 'Ë\x86', 'm', 'V', ')', '.', '*', '<', 'MediaPlayPause', '#', 'C', '{', 'Space', 'ArrowUp', '\x9b', 'PageDown', 'c',
 'ä', '\x97', 'ArrowDown', '^', 'AltGraph', '/', '~', 'e', 'ArrowRight', 'F2', 'AudioVolumeUp', 'Rightclick', '`', '[',
 '(', 'Cancel', 'Pause', 'Shift', 'AudioVolumeMute', 'l', 'x', '¿', 'n', 'ContextMenu', 'I', 'End', 'F12',
 'MediaTrackPrevious', 'Backspace', 'i', '+', 'F', 'ScrollLock', '%', 'd', '\x96', '&', 't', '5', 'AudioVolumeDown',
 'F1', 'MediaTrackNext', '_', 'b', '¡', 'v', 'z', 'A', 'Tab', '-', 'Ä±', 'p', 'ModeChange', 'â\x80\x93', 'a', '$', 'y',
 'Control', '\\', '2', 'F15', 'k', 'Enter', 'Delete', 'M', '@', 'F11', 'o', '0', "'", '1', 'Dead', '"', 'F6', 'T', 'h',
 'r', '}', '>', ':', 'g', 'S', 'Process', 'PageUp', '?', 'Clear', 'Alt', '|'}