from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_d, SDL_KEYUP, SDLK_a

import game_world
import game_framework

from state_machine import StateMachine
import pokemon

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a



# Player1의 Run Speed 계산

# Player1 Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player1 Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8







class Idle:

    def __init__(self, Player1):
        self.Player1 = Player1

    def enter(self, e):
        self.Player1.dir = 0

    def exit(self, e):
        pass


    def do(self):
        self.Player1.frame = (self.Player1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    def draw(self):
        frame_num = int(self.Player1.frame)
        if self.Player1.face_dir == 1:  # right
            self.Player1.image.clip_composite_draw(int(pokemon.mewtwo_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['y']),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['width']),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player1.x,
                                                   self.Player1.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player1.image.clip_draw(int(pokemon.mewtwo_data['sprites'][frame_num]["x"]),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['y']),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['width']),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['height']), self.Player1.x,
                                         self.Player1.y, 100,
                                         100)


class Jump:

    def __init__(self, Player1):
        self.Player1 = Player1

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass


    def handle_event(self, event):
        pass

    def draw(self):
        frame_num = int(self.Player1.frame)
        if self.Player1.face_dir == 1:  # right
            self.Player1.image.clip_composite_draw(int(pokemon.mewtwo_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['y']),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['width']),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player1.x,
                                                   self.Player1.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player1.image.clip_draw(int(pokemon.mewtwo_data['sprites'][frame_num]["x"]),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['y']),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['width']),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['height']), self.Player1.x,
                                         self.Player1.y, 100,
                                         100)



class Run:
    def __init__(self, Player1):
        self.Player1 = Player1

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.Player1.dir = self.Player1.face_dir = 1
        elif left_down(e) or right_up(e):
            self.Player1.dir = self.Player1.face_dir = -1

    def exit(self, e):
        if space_down(e):
            self.Player1.fire_ball()

    def do(self):
        self.Player1.frame = 5+(self.Player1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.Player1.x += self.Player1.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        frame_num = int(self.Player1.frame)
        if self.Player1.face_dir == 1:  # right
            self.Player1.image.clip_composite_draw(int(pokemon.mewtwo_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['y']),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['width']),
                                                   int(pokemon.mewtwo_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player1.x,
                                                   self.Player1.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player1.image.clip_draw(int(pokemon.mewtwo_data['sprites'][frame_num]["x"]),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['y']),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['width']),
                                         int(pokemon.mewtwo_data['sprites'][frame_num]['height']), self.Player1.x,
                                         self.Player1.y, 100,
                                         100)






class Player1:
    def __init__(self):
        self.mycharacter = pokemon.Mewtwo()
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = self.mycharacter.image

        self.IDLE = Idle(self)
        self.JUMP = Jump(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {space_down: self.JUMP, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN : {space_down: self.JUMP,right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
            }
        )



    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        # if group == 'Player1:ball':
        #     self.ball_count += 1
        # if group == 'Player1:zombie':
        #     game_framework.quit()
        pass

