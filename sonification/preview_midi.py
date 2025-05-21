import pygame
import asyncio
import random
import numpy as np
import matplotlib.pyplot as plt

async def start_preview(midi_file, bpm):
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()
    try:
        last_index = 0
        while pygame.mixer.music.get_busy():
            elapsed_time = pygame.mixer.music.get_pos() / 1000.0 # ms -> s
            actual_index = int(elapsed_time / (60 / bpm))
            if actual_index >= last_index:
                last_index = actual_index
                yield last_index + 1 

            pygame.time.Clock().tick(60)
    except asyncio.CancelledError:
        print("Task was canceled.")
        
def stop_preview():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()