import midiutil.MidiFile
import pretty_midi as md #uses setuptools as a dependency, only used for note name to value transfo
import midiutil
import random
from sonification.SonificationConfig import SonificationConfig

def map_value(value, min_value, max_value, min_result, max_result):
    result = min_result + (value - min_value)/max(1,(max_value - min_value))*(max_result - min_result)
    return round(result)

def tuples_to_midi(data, config: SonificationConfig):
    x_coordinates = [x[0] for x in data]
    y_coordinates = [y[1] for y in data]

    note_values = []
    for note in config.note_names:
        note_values.append(md.note_name_to_number(note))

    midi_file = midiutil.MIDIFile(1) #1 track
    midi_file.addTempo(track=0, time=0,tempo=config.bpm)
    midi_file.addProgramChange(0, 0, 0, config.instrument)

    pitch_mapped_data = [map_value(y, min(y_coordinates), max(y_coordinates), 0, len(note_values)-1) for y in y_coordinates] if config.relative_pitch_mapping else [map_value(y, 0, 255, 0, len(note_values)-1) for y in y_coordinates]

    volume_mapped_data = [map_value(y, min(y_coordinates), max(y_coordinates), config.min_velocity, config.max_velocity) for y in y_coordinates]

    i = 0
    while i < len(y_coordinates):
        if config.merge_long_notes:
            same_note_streak = 1
            for j in range(i, len(pitch_mapped_data) - 1):
                if pitch_mapped_data[j] == pitch_mapped_data[j + 1]:
                    same_note_streak += 1
                else:
                    break
            midi_file.addNote(
                track=0,
                channel=0,
                time=x_coordinates[i],
                pitch=note_values[pitch_mapped_data[i]],
                volume=volume_mapped_data[i] if config.relative_velocity_mapping else random.randrange(80,120),
                duration=same_note_streak
            )
            i += same_note_streak
        else:
            midi_file.addNote(
                track=0,
                channel=0,
                time=x_coordinates[i],
                pitch=note_values[pitch_mapped_data[i]],
                volume=volume_mapped_data[i] if config.relative_velocity_mapping else random.randrange(80,120),
                duration=1
            )
            i += 1
            
    from io import BytesIO
    midi_file_bytes = BytesIO()
    midi_file.writeFile(midi_file_bytes)
    midi_file_bytes.seek(0)
    return midi_file_bytes, pitch_mapped_data