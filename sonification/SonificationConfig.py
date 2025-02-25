from dataclasses import dataclass
from sonification import scales

@dataclass
class SonificationConfig:
    grid_rows=8
    grid_cols=8
    process_rgb=False
    merge_long_notes=False
    note_names = scales.scales['chromatic']
    relative_pitch_mapping=True
    relative_velocity_mapping=True
    bpm = 180
    instrument = 0
    min_velocity = 0
    max_velocity = 127
    render_grid = True