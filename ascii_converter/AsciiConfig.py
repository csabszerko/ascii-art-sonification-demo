from dataclasses import dataclass
from PIL import ImageFont

@dataclass
class AsciiConfig:
    text_size_px = 16
    character_map = ' .oO0'
    text_font_path = './ascii_converter/fonts/courier.ttc'
    use_custom_background_color = False
    custom_background_color_bgr=(0, 0, 0)
    use_custom_text_color= False
    custom_text_color_bgr = (255, 255, 255)
    use_edges = False
    only_use_edges = False
    edge_detection_threshold_min = 100
    edge_detection_threshold_max = 180
    
    def get_text_font(self):
        return ImageFont.truetype(self.text_font_path, self.text_size_px)