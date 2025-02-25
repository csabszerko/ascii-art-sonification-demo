import streamlit as st
import cv2 as cv
import numpy as np
from PIL import ImageColor
import pyperclip
from ascii_converter import ascii_with_edges as ascii
from ascii_converter.AsciiConfig import AsciiConfig

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        
        #copy-button.st-copy-to-clipboard-btn {
            /* Your CSS styles here */
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.title('ASCII Art generator')
uploaded_image = st.file_uploader('Upload your image', type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)

if uploaded_image is not None:
    config = AsciiConfig()
    
    with st.container(border=True):
        config.text_size_px = st.number_input('Font size', min_value=1, value=64)

        preset_column, invert_checkbox_column = st.columns([6, 1], vertical_alignment='bottom')

        preset_options = ['Custom value',
                            ' .oO',
                            ' .:-=+*#%@',
                            ' .:=-+*$ZODXWM8&%#@',
                            ' .,"^;lI!i<>~+-?_][]{}1()|\ftjrxnuvzYXUJCQL0ZWmqwpdkao*#MW&8%B@$',
                            ' .-`:_,^=;><+!rc*/z?sLTv)J7(|F{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@']

        selected_preset = preset_column.selectbox('Character map presets', preset_options)

        if selected_preset == 'Custom value':
            custom_character_map = st.text_input('Enter your custom value', value=preset_options[1])
            if custom_character_map:
                config.character_map = custom_character_map
            else:
                st.error('Enter a value!')
        else:
            config.character_map = selected_preset

        invert_checkbox = invert_checkbox_column.checkbox('Invert')

        if invert_checkbox:
            config.character_map = config.character_map[::-1]
        
    with st.container(border=True):
        selected_edge_preset = st.radio('Edges', ['No edges', 'Use edges', 'Only use edges'])
        
        if(selected_edge_preset != 'No edges'):
            if(selected_edge_preset == 'Use edges'):
                config.use_edges = True
            elif(selected_edge_preset == 'Only use edges'):
                config.use_edges = True
                config.only_use_edges = True
            edge_detection_thresholds = st.slider('Edge detection thresholds', value=[0, 255])
            config.edge_detection_threshold_min = edge_detection_thresholds[0]
            config.edge_detection_threshold_max = edge_detection_thresholds[1]
        
    with st.container(border=True):
        col1, spacer, col2 = st.columns([5, 1, 5], vertical_alignment='center')

        # First column: Text color settings
        with col1:
            col3, col4 = st.columns([5, 1])
            with col3:
                use_custom_text_color_checkbox = st.checkbox('Swap text color')
                config.use_custom_text_color = use_custom_text_color_checkbox
            with col4: 
                config.custom_text_color_bgr = ImageColor.getrgb(
                st.color_picker(
                    'Text color', '#ffffff',
                    disabled=not use_custom_text_color_checkbox,
                    label_visibility='collapsed'
                ))[::-1]
                
        with spacer:
            st.empty()
            
        with col2:
            col5, col6 = st.columns([5, 1])
            with col5:
                use_custom_background_color_checkbox = st.checkbox('Swap background color')
                config.use_custom_background_color = use_custom_background_color_checkbox
            with col6: 
                config.custom_background_color_bgr = ImageColor.getrgb(
                st.color_picker(
                    'Background Color', '#000000',
                    disabled=not use_custom_background_color_checkbox,
                    label_visibility='collapsed'
                ))[::-1]
                
    # convert the uploaded file to a numpy array
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    
    # numpy array to an opencv image
    image = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    
    ascii_image, ascii_image_text = ascii.image_to_ascii(image, config)
    
    with st.container(border=True):
        original_image, arrow, result_image = st.columns([5,1,5], vertical_alignment='center')
        with original_image:
            st.image(image, caption="Original Image", channels="BGR", use_container_width=True)

        with arrow:
            st.markdown('<span style="font-size: 48px; text-align: center; color: gray;">-></span>', unsafe_allow_html=True)

        with result_image:
            st.image(ascii_image, caption="ASCII Image", channels='BGR', use_container_width=True)
            
    _, copy_to_clipboard_button = st.columns([6,5])
    with copy_to_clipboard_button:
        clicked = st.button('Copy as text to clipboard', on_click=(pyperclip.copy(ascii_image_text)),  use_container_width=True)
        if clicked:
            st.markdown('<span style="text-align: center; font-size: .8rem; color: #907ad6;"> Copied to clipboard!</span>', unsafe_allow_html=True)