#!/usr/bin/env python
# coding: utf-8

import music21

class Instrument:
    FRET_COUNT = 30
    
    tuning = []
    fretboard = {}

    def __init__(self, name, strings):
        self.name = name
        self.__set_tuning(strings)    

    def get_tuning(self):
        return self.tuning
    
    def get_note(self, string, fret):
        return self.fretboard[self.__get_key(string - 1, fret)]
        #return self.tuning[string - 1].transpose(fret)
    
    def __set_tuning(self, strings): 
        self.tuning = []
        for string in strings:
            self.tuning.append(music21.note.Note(str(string)))
            
        self.fretboard = {}
        for string in range(len(self.tuning)):
            for fret in range(0, self.FRET_COUNT):
                self.fretboard[self.__get_key(string, fret)] = self.tuning[string].transpose(fret)
            
    def __get_key(self, string, fret):
        return str(string) + '-' + str(fret)
            
