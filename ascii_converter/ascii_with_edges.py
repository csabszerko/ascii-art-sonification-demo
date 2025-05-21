from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
import numpy as np
from . import AsciiConfig


def gradient_to_char(angle):
    angle = angle % 360

    if (0 <= angle < 22.5) or (337.5 <= angle < 360) or (157.5 <= angle < 202.5):
        return '|'
    elif (22.5 <= angle < 67.5) or (202.5 <= angle < 247.5):
        return '/'
    elif (67.5 <= angle < 112.5) or (247.5 <= angle < 292.5):
        return '-'
    elif (112.5 <= angle < 157.5) or (292.5 <= angle < 337.5):
        return '\\'
    return ' '

def image_to_ascii(np_img, config: AsciiConfig):
    
    h, w = np_img.shape[:2]
    
    config.text_size_px = min(config.text_size_px, min(h, w))

    downsampled_w = w // config.text_size_px
    downsampled_h = h // config.text_size_px


    np_img = cv.resize(np_img, (downsampled_w, downsampled_h), cv.INTER_NEAREST)
    np_img_gray = cv.cvtColor(np_img, cv.COLOR_BGR2GRAY)

    result_str = ""

    edges = cv.Canny(np_img_gray, config.edge_detection_threshold_min, config.edge_detection_threshold_max)

    Gx = cv.Sobel(np_img_gray, cv.CV_64F, 1, 0, ksize=3) 
    Gy = cv.Sobel(np_img_gray, cv.CV_64F, 0, 1, ksize=3)

    magnitude = np.sqrt(Gx**2 + Gy**2)
    orientation = np.arctan2(Gy, Gx)

    masked_magnitude = magnitude * (edges > 0) 
    masked_magnitude[masked_magnitude > 0] = 255 

    masked_orientation = orientation * (edges > 0)
    masked_orientation_degrees = np.degrees(masked_orientation)

    result_img = Image.new('RGB', (downsampled_w*config.text_size_px, downsampled_h*config.text_size_px), config.custom_background_color_bgr if config.use_custom_background_color else (0,0,0)) # multiply to nearest multiple of the text size, so that text is never out of bounds
    result_img_renderer = ImageDraw.Draw(result_img)

    for y in range(downsampled_h):
        for x in range(downsampled_w):
            b,g,r = np_img[y, x]
            brightness = np_img_gray[y, x]
            character = config.character_map[int(len(config.character_map) * (brightness / 256))]
            if(config.use_edges):
                if(edges[y,x]>0):
                    current_degree = masked_orientation_degrees[y,x]
                    character = gradient_to_char(current_degree)
                elif(config.only_use_edges):
                        character = ' '
                        
            result_str += character
            result_img_renderer.text(
                (x*config.text_size_px+config.text_size_px/6,
                y*config.text_size_px),
                character,
                font=config.get_text_font(),
                fill=config.custom_text_color_bgr
                if config.use_custom_text_color 
                else (b,g,r))
        result_str += '\n'
    return np.asarray(result_img), result_str