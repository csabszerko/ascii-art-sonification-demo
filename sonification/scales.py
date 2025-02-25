scales = {
    # only sharps, no flats
    "chromatic": ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],

    "C_major": ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    "C_minor": ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#'],

    "C#_major": ['C#', 'D#', 'F', 'F#', 'G#', 'A#', 'C'],
    "C#_minor": ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'],

    "D_major": ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    "D_minor": ['D', 'E', 'F', 'G', 'A', 'A#', 'C'],

    "D#_major": ['D#', 'F', 'F#', 'G#', 'A#', 'C', 'D'],
    "D#_minor": ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#'],

    "E_major": ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    "E_minor": ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],

    "F_major": ['F', 'G', 'A', 'A#', 'C', 'D', 'E'],
    "F_minor": ['F', 'G', 'G#', 'A#', 'C', 'C#', 'D#'],

    "F#_major": ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E'],
    "F#_minor": ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],

    "G_major": ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    "G_minor": ['G', 'A', 'A#', 'C', 'D', 'D#', 'F'],

    "G#_major": ['G#', 'A#', 'C', 'C#', 'D#', 'F', 'F#'],
    "G#_minor": ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#'],

    "A_major": ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    "A_minor": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],

    "A#_major": ['A#', 'C', 'D', 'D#', 'F', 'G', 'A'],
    "A#_minor": ['A#', 'C', 'C#', 'D#', 'F', 'F#', 'G#'],

    "B_major": ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
    "B_minor": ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
}


def get_key_octaves(notes, octave_range):
    notes_array = []
    for i in range(octave_range[0], octave_range[1]+1):
        for note in notes:
            notes_array.append(f"{note}{i}")
    return notes_array