#!/usr/bin/env python
# coding: utf-8

from src.gpparser.block import Block
from src.gpparser.eventFactory import EventFactory
from src.gpparser.events import *
from src.gpparser.instrument import *
import guitarpro
from music21 import duration as mduration


class GpParser:
    BASS_INSTRUMENT = 'bass'
    BASS_MIDI_INSTRUMENT = range(33, 40) #https://www.midi.org/specifications/item/gm-level-1-sound-set
     
    def parse_song(self, file):
        song = guitarpro.parse(file)
        events = []
        track = self.__get_bass_track(song)
        if not track:
            print('bass track not found')
            return events

        bass = Instrument(self.BASS_INSTRUMENT, track.strings)
        event_factory = EventFactory(bass)

        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    block = self.__create_block(event_factory, beat)
                    events.append(block.to_dict())
 
        return events

    def __create_block(self, event_factory, beat):
        block = Block(beat)
        if block.is_normal_beat:
            events = event_factory.create(beat)
            block.add_events(events)

        return block

    def __is_bass_midi_instrument(self, instrument):
        if instrument in self.BASS_MIDI_INSTRUMENT:
            return True
        return False

    def __get_bass_track(self, song):
        for track in song.tracks:
            if self.__is_bass_midi_instrument(track.channel.instrument) or self.BASS_INSTRUMENT in track.name.lower():
                return track
            


    
