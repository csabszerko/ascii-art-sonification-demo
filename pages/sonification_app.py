import streamlit as st
import cv2 as cv
import numpy as np
import asyncio
import matplotlib.pyplot as plt
from sonification import image_data_processing, scales
from sonification.preview_midi import start_preview, stop_preview
from sonification.SonificationConfig import SonificationConfig


hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.title('Sonification')
stop_preview() #stop running midi
uploaded_image = st.file_uploader('Upload your image', type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)

if uploaded_image is not None:
    config = SonificationConfig()
    
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)

    # numpy array to an opencv image
    image = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    
    with st.container(border=True):
        st.write('Midi settings')
        preset_column, octave_input = st.columns([1, 2], vertical_alignment='top')
        
        preset_options = scales.scales.keys() 
        selected_preset = preset_column.selectbox('Key presets', preset_options)
        
        all_note_options = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
        
        displayable_notes_from_preset = []
        
        for preset_note in scales.scales[selected_preset]:
            for displayable_note in all_note_options:
                if preset_note in displayable_note.split('/'):
                    displayable_notes_from_preset.append(displayable_note)
                
        selected_notes = [note.split('/')[0] for note in sorted(st.segmented_control('Select your notes',
                                            options=all_note_options,
                                            default=displayable_notes_from_preset,
                                            selection_mode='multi'), key=lambda note: all_note_options.index(note))]
        
        octave_range = octave_input.slider('Octave range', value=[0, 5], min_value=0, max_value=5)
        
    if selected_notes:     
        selected_notes_with_octaves = scales.get_key_octaves(selected_notes, octave_range)
        config.note_names = selected_notes_with_octaves
        with st.container(border=True):
            st.write('Image processing settings')
            col1, col2 = st.columns([1,1], vertical_alignment='bottom', gap='small')
            with col1:
                config.grid_rows = st.number_input('Grid rows',  min_value=1, max_value=512, value=8)
            with col2:
                config.grid_cols = st.number_input('Grid columns',  min_value=1, max_value=512, value=8)
                
            config.relative_pitch_mapping = st.checkbox('Normalize pitch mapping', value=True)
            config.relative_velocity_mapping = st.checkbox('Custom velocity mapping', value=True)
            if config.relative_velocity_mapping:
                velocity_range = st.slider('Velocity range', value=[0, 127], min_value=0, max_value=127)
                config.min_velocity = velocity_range[0]
                config.max_velocity = velocity_range[1]
            config.process_rgb = st.checkbox('Use RGB channels to make chords')
            config.merge_long_notes = st.checkbox('Merge adjacent notes into one long note')
            
        with st.container(border=True):
            st.write('Preview settings')
            col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment='bottom', gap='small')
            with col1:
                config.bpm = st.number_input('BPM',  min_value=1, max_value=1000, value=180)
            with col2:
                config.instrument = st.number_input('Midi instrument index',  min_value=0, max_value=127, value=0)
            with col3:
                config.render_grid = st.checkbox('Render grid')
            
            
            result_midi, plot_image_buffer, cell_image_buffer = image_data_processing.image_to_midi(image, config)
            # print(len(plot_image_buffer), len(cell_image_buffer))
            
            plot_container = st.empty()
            if not config.process_rgb:
                plot_container.image(plot_image_buffer[0], channels="BGR", use_container_width=True)
            
            image_container = st.empty()
            image_container.image(cell_image_buffer[0], caption="Original Image", channels="BGR", use_container_width=True)
        
            col1, col2 = st.columns([1,1])
            with col1:
                st.download_button(
                    label="Download MIDI file",
                    data=result_midi,
                    file_name="generated_midi.mid",
                    mime="audio/midi",
                    use_container_width=True)
            with col2:
                placeholder = st.empty()
                with placeholder:
                    if st.button('Play preview', use_container_width=True):
                        if st.button('Stop', use_container_width=True):
                            stop_preview()
                        async def handle_async():
                            async for value in start_preview(result_midi, config.bpm):
                                # print(value)
                                if value<len(cell_image_buffer):
                                    image_container.image(cell_image_buffer[value if value<len(cell_image_buffer) else len(cell_image_buffer)-1], caption="Original Image", channels="BGR", use_container_width=True)
                                    if not config.process_rgb: 
                                        plot_container.image(plot_image_buffer[value if value<len(plot_image_buffer) else len(plot_image_buffer)-1], channels="BGR", use_container_width=True)
                        loop = asyncio.new_event_loop()
                        try:
                            asyncio.set_event_loop(loop)
                            loop.run_until_complete(handle_async())
                        finally:
                            # st.rerun()
                            # print('playback finished')
                            # print("event loop closed")
                            loop.close()
                            # st.rerun()
                            if st.button('Play preview', use_container_width=True, key='after_playback'):
                                st.rerun()
                        
    else:
        st.error('Select a note!')
            
    st.markdown('<a href="https://en.wikipedia.org/wiki/General_MIDI#Piano" style="color: #907ad6;"> Help with instruments </a>', unsafe_allow_html=True)
# st.page_link('pages/ascii_app.py', label='Check out my ASCII art generator as well')
