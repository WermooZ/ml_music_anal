#!/usr/bin/env python
# coding: utf-8

DEAD_EVENT = 'dead'
REST_NAME = 'R'
DEAD_NAME = 'X'

class Event():
    name = ''
    octave = ''
    meta = {}
    
    def __init__(self, note):
        self.type = note.type.name
        #self.__add_meta(note)
        
    def to_dict(self):
        return  self.__dict__
    
    def __add_meta(self, note):
        self.meta = {
            'ghostNote' : int(note.effect.ghostNote),
            'hammer'    : int(note.effect.hammer),
            'palmMute'  : int(note.effect.palmMute),
            'slides'    : len(note.effect.slides)
        }
          
        
class DeadEvent(Event):
    def __init__(self, note):
        super().__init__(note)
        self.name = DEAD_NAME
        
        
class NoteEvent(Event):
    def __init__(self, note, music_note):
        super().__init__(note)
        
        self.name = music_note.name
        self.octave = music_note.octave



