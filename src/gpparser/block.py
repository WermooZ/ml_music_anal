#!/usr/bin/env python
# coding: utf-8

import music21
from src.gpparser.events import *


class Block():
    def __init__(self, duration):
        self.duration = duration
        self.events = []
        
    def __add_event(self, event):
        self.events.append(event)
        
    def get_chord_info(self):
        if len(self.events) > 1:
            c = music21.chord.Chord()
            for event in self.events:
                if type(event) == DeadEvent:
                    return ''
                c.add(event.name)
            return c.commonName
        
    def to_dict(self):
        root_event = self.events[0]
        data = root_event.meta
        data['duration']    = self.duration
        data['no_of_notes'] = len(self.events)
        data['root_name']   = root_event.name
        data['root_octave'] = root_event.octave
        data['root_midi']   = root_event.midi
        #data['root_freq']   = root_event.frequency
        
        if len(self.events) > 1 :
            data['chord']     = self.get_chord_info()
            data['scnd_note'] = self.events[1].name
            #data['scnd_freq'] = self.events[1].frequency
            
        return data

    def add_events(self, eventFactory, beat):
        for event in eventFactory.create2(beat):
            self.__add_event(event)
