from pico2d import load_image, get_time, load_font, draw_rectangle

import game_world
import game_framework
import json

with open('Mewtwo_data.json', 'r', encoding='utf-8') as f:
    mewtwo_data = json.load(f)

with open('Gengar_data.json', 'r', encoding='utf-8') as f:
    gengar_data = json.load(f)

# Mewtwo의 Run Speed 계산

# Mewtwo Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Mewtwo Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Mewtwo:
    def __init__(self):
        self.image = load_image('Mewtwo.png')

class Gengar:
    def __init__(self):
        self.image = load_image('Gengar.png')
