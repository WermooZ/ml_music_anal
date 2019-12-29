#!/usr/bin/env python
# coding: utf-8

import music21
import guitarpro


DEAD_EVENT = 'dead'
REST_NAME = 'R'
DEAD_NAME = 'X'

class Event():
    name = ''
    octave = ''
    frequency = ''
    midi = ''
    meta = {}


class RestEvent(Event):
    def __init__(self):
        self.name = REST_NAME
        
class NoteEvent(Event):
    def __init__(self, note, meta):
        self.name = note.name
        self.note = note.nameWithOctave
        self.octave = note.octave
        self.frequency = self.__get_frequency(note)
        self.midi = self.__get_midi(note)
        self.meta = meta
        
    def __get_frequency(self, note):
        p1 = music21.pitch.Pitch(note.nameWithOctave)

        return str(p1.frequency)

    def __get_midi(self, note):
        p1 = music21.pitch.Pitch(note.nameWithOctave)

        return str(p1.midi)
        
class DeadEvent(Event):
    def __init__(self, meta):
        self.name = DEAD_NAME
        self.meta = meta
        
class EventFactory():
    def __init__(self, instrument):
        self.instrument = instrument
        
    def __create_note(self, note):
        meta = {
            'type'      : note.type.name,
            'ghostNote' : int(note.effect.ghostNote),
            'hammer'    : int(note.effect.hammer),
            'palmMute'  : int(note.effect.palmMute),
            'slides'    : len(note.effect.slides)
        }
        
        if note.type.name == DEAD_EVENT:
            return DeadEvent(meta)

        return NoteEvent(self.instrument.get_note(note.string, note.value), meta)

    def create(self, beat):
        events = []
        if beat.status == guitarpro.BeatStatus.rest:
            events.append(RestEvent())
        else:
            for note in beat.notes[::-1]:
                events.append(self.__create_note(note))

        return events


