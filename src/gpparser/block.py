#!/usr/bin/env python
# coding: utf-8

import music21
from src.gpparser.events import *
from music21 import duration as mduration
import guitarpro
import numpy as np

REST_NAME = 'R'

DEFAULT_VALUES = {
    'type': 'normal',   
    'duration' : 0,
    'name' : REST_NAME,
    'octave' : np.nan
}

class Block():
    def __init__(self, beat):
        self.duration = self.__get_duration(beat)
        self.is_normal_beat = self.__is_normal_beat(beat)
        self.events = []

    def to_dict(self):
        data = {**DEFAULT_VALUES}
        
        data['duration'] = self.duration
        if self.is_normal_beat:
            root_event = self.events[0]
            data.update(root_event.to_dict())
         
        return data
        
        
    def __get_chord_info(self):
        c = music21.chord.Chord()
        for event in self.events:
            if type(event) == DeadEvent:
                return ''
            c.add(event.name)
        return c.commonName
        
    def add_events(self, events):
        for event in events:
            self.events.append(event)

    def __get_duration(self, beat):
        tuplet = beat.duration.tuplet
        tupletValue = tuplet.times / tuplet.enters
        duration = mduration.Duration(4 / beat.duration.value * tupletValue)
        if beat.duration.isDotted:
            duration.dots = 1

        return float(duration.quarterLength)

    def __is_normal_beat(self, beat):
        return beat.status == guitarpro.BeatStatus.normal
    
