#!/usr/bin/env python
# coding: utf-8

import music21

class Instrument:
    tuning = []
    def __init__(self, name, strings):
        self.name = name
        self.tuning = []

        for string in strings:
            self.add_string(str(string))
    
    def __add_string(self, note):
        self.tuning.append(music21.note.Note(note))
    
    def get_tuning(self):
        return self.tuning
    
    def get_note(self, string, fret):
        return self.tuning[string - 1].transpose(fret)
