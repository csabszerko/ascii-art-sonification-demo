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
    # plt.scatter(x_coordinates, y_coordinates, s=y_coordinates)
    # plt.show()

    #convert to midi values
    note_values = []
    for note in config.note_names:
        note_values.append(md.note_name_to_number(note))

    # print(note_values)

    #new midi obj

    midi_file = midiutil.MIDIFile(1) #1 track
    midi_file.addTempo(track=0, time=0,tempo=config.bpm)
    midi_file.addProgramChange(0, 0, 0, config.instrument)

    pitch_mapped_data = [map_value(y, min(y_coordinates), max(y_coordinates), 0, len(note_values)-1) for y in y_coordinates] if config.relative_pitch_mapping else [map_value(y, 0, 255, 0, len(note_values)-1) for y in y_coordinates]
    # print("pitch " + str(pitch_mapped_data))

    volume_mapped_data = [map_value(y, min(y_coordinates), max(y_coordinates), config.min_velocity, config.max_velocity) for y in y_coordinates]

    # print(volume_mapped_data)
    i = 0
    while i < len(y_coordinates):
        if config.merge_long_notes:
            same_note_streak = 1
            for j in range(i, len(pitch_mapped_data) - 1):
                if pitch_mapped_data[j] == pitch_mapped_data[j + 1]:
                    same_note_streak += 1
                else:
                    break
            # add the merged long note
            midi_file.addNote(
                track=0,
                channel=0,
                time=x_coordinates[i],
                pitch=note_values[pitch_mapped_data[i]],
                volume=volume_mapped_data[i] if config.relative_velocity_mapping else random.randrange(80,120),
                duration=same_note_streak
            )
            # skip the next different note
            i += same_note_streak
        else:
            # add each note individually, even if its a sequence of the same notes
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
    midi_file_bytes.seek(0)  # Reset pointer to the beginning of the file
    return midi_file_bytes, pitch_mapped_data