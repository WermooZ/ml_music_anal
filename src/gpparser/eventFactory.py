#!/usr/bin/env python
# coding: utf-8

from src.gpparser.events import *


class EventFactory():
    def __init__(self, instrument):
        self.instrument = instrument

    def create(self, beat):
        events = []
        for note in self.__get_notes_from_lowest(beat):
            events.append(self.__create_note(note))

        return events

    def __get_notes_from_lowest(self, beat):
        return beat.notes[::-1]

    def __create_note(self, note):
        if note.type.name == DEAD_EVENT:
            return DeadEvent(note)

        m_note = self.instrument.get_note(note.string, note.value)
        return NoteEvent(note, m_note)


