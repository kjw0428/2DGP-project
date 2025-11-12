from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_w, SDLK_s

import game_world
import game_framework

from state_machine import StateMachine
import pokemon

def w_down(e): # e is w down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def s_down(e): # e is w down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


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
        # 점프 물리값 (픽셀 단위)
        self.jump_speed = 700.0  # 초기 점프 속도 (pixels/s)
        self.gravity = -2500.0   # 중력 (pixels/s^2)
        self.ground_y = 90

    def enter(self, e):
        # 지면에 있을 때만 점프 시작
        if self.Player1.y <= self.ground_y + 1:
            self.Player1.vy = self.jump_speed
            self.Player1.frame = 0

    def exit(self, e):
        # 착지 시 속도 초기화
        self.Player1.vy = 0

    def do(self):
        dt = game_framework.frame_time
        # 애니메이션(Idle의 프레임 수 사용)
        self.Player1.frame = (self.Player1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % 5
        # 물리 계산
        self.Player1.vy += self.gravity * dt
        self.Player1.y += self.Player1.vy * dt
        # 공중에서도 좌우 이동 유지
        self.Player1.x += self.Player1.dir * RUN_SPEED_PPS * dt

        # 착지 검사
        if self.Player1.y <= self.ground_y:
            try:
                self.Player1.state_machine.cur_state.exit(('LAND', None))
            except Exception:
                pass
            self.Player1.y = self.ground_y
            self.Player1.vy = 0
            self.Player1.state_machine.cur_state = self.Player1.IDLE
            try:
                self.Player1.state_machine.cur_state.enter(('LAND', None))
            except Exception:
                pass


    def handle_event(self, event):
        # ('INPUT', sdl_event) 형태로 전달됨
        e = event
        if isinstance(e, tuple) and e[0] == 'INPUT':
            ev = e[1]
        else:
            ev = e
        if ev.type == SDL_KEYDOWN:
            if ev.key == SDLK_d:
                self.Player1.dir = 1
                self.Player1.face_dir = 1
            elif ev.key == SDLK_a:
                self.Player1.dir = -1
                self.Player1.face_dir = -1
        elif ev.type == SDL_KEYUP:
            if ev.key in (SDLK_d, SDLK_a):
                self.Player1.dir = 0

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
        # 점프나 발사 등 다른 행동을 위해 남겨뒀던 공간, 현재는 사용 안 함
        pass

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
        self.vy = 0.0

        self.IDLE = Idle(self)
        self.JUMP = Jump(self)
        self.RUN = Run(self)
        self.DEFENSE = Defense(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {w_down: self.JUMP, s_down: self.DEFENSE, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN : {w_down: self.JUMP, s_down: self.DEFENSE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
                self.JUMP: {},
                self.DEFENSE: {s_up: self.IDLE}
             }
         )



    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 상태 전이 처리
        self.state_machine.handle_state_event(('INPUT', event))
        # 현재 상태에 추가 이벤트 처리가 있으면 전달
        try:
            cur = self.state_machine.cur_state
            if hasattr(cur, 'handle_event'):
                cur.handle_event(('INPUT', event))
        except Exception:
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
