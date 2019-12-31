#!/usr/bin/env python
# coding: utf-8

import music21
import numpy as np

NOTE_TIE = 'tie'
NOTE_NORMAL = 'normal'
NOTE_DEAD = 'dead'

TYPE_NORMAL = 0
TYPE_DEAD   = 1
TYPE_TIE    = 2

TYPE_DICT = {
    'normal' : TYPE_NORMAL, 
    'dead' : TYPE_DEAD, 
    'tie' : TYPE_TIE
}


def frequency(note): 
    p1 = music21.pitch.Pitch(note.nameWithOctave)

    return p1.frequency

def midi(note): 
    p1 = music21.pitch.Pitch(note.nameWithOctave)

    return p1.midi   

def get_duration(beat):
    tuplet = beat.duration.tuplet
    tupletValue = tuplet.times / tuplet.enters
    duration = music21.duration.Duration(4 / beat.duration.value * tupletValue)
    if beat.duration.isDotted:
        duration.dots = 1

    return float(duration.quarterLength)
        
def calc_octave_range(df):
    series = df['octave'].replace('', np.nan).dropna().astype(int)
    min = series.min()
    max = series.max()
    return  min, max, max - min 

def calc_note_range(song):
    min_midi = song['midi'].min()
    max_midi = song['midi'].max()
    min_note = music21.note.Note(min_midi).nameWithOctave
    max_note = music21.note.Note(max_midi).nameWithOctave
    
    return  min_midi, max_midi, min_note, max_note

def get_closest_value(value, available_values):
    pos = (np.abs(available_values-value)).argmin()

    return available_values[pos]

# strip rests on beginning and end
def trim_nans(df, column_name="octave"):
    first_note = df[column_name].idxmin(skipna=True)
    last_note  = df[column_name][::-1].idxmin(skipna=True) - 1

    return df[first_note:last_note]

def merge_tied_notes(df):
    duration_sum = 0
    duration_adj = []
    for index, row in df[::-1].iterrows():
        if row['type'] == NOTE_TIE:
            duration_sum = duration_sum + row['duration']
            duration_adj.append(row['duration'])
        elif row['type'] == NOTE_NORMAL:
            duration_adj.append(row['duration'] + duration_sum)
            duration_sum = 0
        else:
            duration_adj.append(row['duration'])
        
    durations = duration_adj[::-1]
    df['duration'] = np.array(durations)
    #droping rows
    df = df.drop(df[df['type'] == NOTE_TIE].index)

    return df


def normalize_duration(df, threshold=100, max_quarter=2.0):
    #normalize octave & duration
    df['duration'] = df['duration'].clip(upper=max_quarter)
    
    x = df['duration'].value_counts()
    values_to_process = x[x.lt(threshold)].keys().to_numpy()
    available_values =  x[x.ge(threshold)].keys().to_numpy()
    vals = {}
    for value in values_to_process:
        vals[value] = get_closest_value(value, available_values)
        
    return df.replace(vals)

def extract_columns(df, columns=[]):
    columns_to_remove = list(set(df.columns.values.tolist()) - set(columns))
    return df.drop(columns=columns_to_remove)

def create_event_column(df):
    #create note name
    df['octave'] = df['octave'].fillna('').astype(str)
    df['name'] = (df['name'] + df['octave'])
    
    # create event_name
    df['event'] = (df['name'] + '_'+ df['duration'].astype(str))
    
    return df

def transpose_song(df, transpose_value):
    df['octave'] = df['octave'].replace('', np.nan).fillna(0).astype(int)
    df['octave'] = (df['octave'] - transpose_value)
    df['octave'].clip(lower=0, inplace=True)
    df['octave'].replace(0, '', inplace=True)
    
    return df 

#TODO types for blocks

def type_to_int(df):
    return df.replace(TYPE_DICT)