#!/usr/bin/env python
# coding: utf-8

from src.gpparser.block import Block
from src.gpparser.events import *
from src.gpparser.instrument import *
import guitarpro
from music21 import duration as mduration


class GpParser:
    BASS_INSTRUMENT = 'bass'
    BASS_MIDI_INSTRUMENT = range(33, 40) #https://www.midi.org/specifications/item/gm-level-1-sound-set

    columns = {
        #'artist'      : ''
        #'album'       : '',
        #'title'       : '',
        # effect
        'song'        : '',
        'type'        : '',
        'ghostNote'   : '',
        'hammer'      : '',
        'palmMute'    : '',
        'slides'      : '',
        # note
        'duration'    : '',
        'no_of_notes' : '',
        'chord'       : '',
        'root_note'   : '',
        'root_name'   : '',
        'root_octave' : '',
        'root_midi' : '',
        #'root_freq'   : '',
        'scnd_note'   : '',
        'scnd_freq'   : ''
    }
    seperator = ','
     
    def parse_song(self, file):
        song = guitarpro.parse(file)
        events = []
        track = self.__get_bass_track(song)
        if not track:
            print('bass track not found')
            return events

        bass = Instrument(self.BASS_INSTRUMENT, track.strings)
        eventFactory = EventFactory(bass)

        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    block = self.__create_block(eventFactory, beat)

                    if len(block.events): #TODO - refactor this
                        result = block.to_dict()
                        for k, v in result.items():
                            result.update({k:str(v)})

                        allColumns = self.columns.copy()
                        allColumns.update(result)

                        events.append(allColumns)
        return events

    def __create_block(self, eventFactory, beat):
        block = Block(self.__get_duration(beat))
        block.add_events(eventFactory, beat)

        return block

    def __is_bass_midi_instrument(self, instrument):
        if instrument in self.BASS_MIDI_INSTRUMENT:
            return True
        return False

    def __get_bass_track(self, song):
        for track in song.tracks:
            if self.__is_bass_midi_instrument(track.channel.instrument) or self.BASS_INSTRUMENT in track.name.lower():
                return track
            

    def __get_duration(self, beat):
        tuplet = beat.duration.tuplet
        tupletValue = tuplet.times / tuplet.enters
        duration = mduration.Duration(4 / beat.duration.value * tupletValue)
        if beat.duration.isDotted:
            duration.dots = 1
        return float(duration.quarterLength)
    
