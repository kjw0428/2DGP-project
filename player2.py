from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN

import game_world
import game_framework

from state_machine import StateMachine
import pokemon

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def down_down(e): # e is w down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

# Player2의 Run Speed 계산

# Player2 Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player2 Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8







class Idle:

    def __init__(self, Player2):
        self.Player2 = Player2

    def enter(self, e):
        self.Player2.dir = 0

    def exit(self, e):
        pass


    def do(self):
        # player1과 동일하게 Idle 애니메이션은 5 프레임 사용
        self.Player2.frame = (self.Player2.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    def draw(self):
        frame_num = int(self.Player2.frame)
        if self.Player2.face_dir == 1:  # right
            self.Player2.image.clip_composite_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player2.x,
                                                   self.Player2.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player2.image.clip_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                         int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['height']), self.Player2.x,
                                         self.Player2.y, 100,
                                         100)


class Jump:
    def __init__(self, Player2):
        self.Player2 = Player2
        # 점프 물리값
        self.jump_speed = 700.0
        self.gravity = -2500.0
        self.ground_y = 90

    def enter(self, e):
        # 지면에 있을 때만 점프 시작
        if self.Player2.y <= self.ground_y + 1:
            self.Player2.vy = self.jump_speed
            self.Player2.frame = 0

    def exit(self, e):
        # 착지 시 속도 초기화
        self.Player2.vy = 0

    def do(self):
        dt = game_framework.frame_time
        # player1과 동일하게 Idle 애니메이션 프레임 수(5) 사용
        self.Player2.frame = (self.Player2.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % 3
        # 물리 업데이트
        self.Player2.vy += self.gravity * dt
        self.Player2.y += self.Player2.vy * dt
        self.Player2.x += self.Player2.dir * RUN_SPEED_PPS * dt

        # 착지 검사
        if self.Player2.y <= self.ground_y:
            try:
                self.Player2.state_machine.cur_state.exit(('LAND', None))
            except Exception:
                pass
            self.Player2.y = self.ground_y
            self.Player2.vy = 0
            self.Player2.state_machine.cur_state = self.Player2.IDLE
            try:
                self.Player2.state_machine.cur_state.enter(('LAND', None))
            except Exception:
                pass

    def handle_event(self, event):
        e = event
        if isinstance(e, tuple) and e[0] == 'INPUT':
            ev = e[1]
        else:
            ev = e
        if ev.type == SDL_KEYDOWN:
            if ev.key == SDLK_RIGHT:
                self.Player2.dir = 1
                self.Player2.face_dir = 1
            elif ev.key == SDLK_LEFT:
                self.Player2.dir = -1
                self.Player2.face_dir = -1
        elif ev.type == SDL_KEYUP:
            if ev.key in (SDLK_RIGHT, SDLK_LEFT):
                self.Player2.dir = 0

    def draw(self):
        frame_num = int(self.Player2.frame)
        if self.Player2.face_dir == 1:  # right
            self.Player2.image.clip_composite_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player2.x,
                                                   self.Player2.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player2.image.clip_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                         int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['height']), self.Player2.x,
                                         self.Player2.y, 100,
                                         100)

class Run:
    def __init__(self, Player2):
        self.Player2 = Player2

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.Player2.dir = self.Player2.face_dir = 1
        elif left_down(e) or right_up(e):
            self.Player2.dir = self.Player2.face_dir = -1

    def exit(self, e):
        # player1과 동일하게 exit에서는 특수 동작 없음
        pass

    def do(self):
        # player1과 동일하게 Run 애니메이션은 3프레임(인덱스 5~7) 사용
        self.Player2.frame = 4+(self.Player2.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9
        self.Player2.x += self.Player2.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        frame_num = int(self.Player2.frame)
        if self.Player2.face_dir == 1:  # right
            self.Player2.image.clip_composite_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player2.x,
                                                   self.Player2.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player2.image.clip_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                         int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['height']), self.Player2.x,
                                         self.Player2.y, 100,
                                         100)


class Defense:
    def __init__(self, Player2):
        self.Player2 = Player2

    def enter(self, e):
        # 방어 시작: 고정 프레임 사용
        self.Player2.frame = 19
        # 정지 상태로 만들려면 이동을 0으로
        self.Player2.dir = 0

    def exit(self, e):
        # 방어 해제 시 특별 처리 없음
        pass

    def do(self):
        # 고정된 방어 프레임 유지
        self.Player2.frame = 16

    def handle_event(self, event):
        # 공중/방어 중에도 방향키 입력을 받아 방향 전환만 처리
        e = event
        if isinstance(e, tuple) and e[0] == 'INPUT':
            ev = e[1]
        else:
            ev = e
        if ev.type == SDL_KEYDOWN:
            if ev.key == SDLK_RIGHT:
                self.Player2.face_dir = 1
            elif ev.key == SDLK_LEFT:
                self.Player2.face_dir = -1
        # s_up는 상태전이 맵으로 처리되므로 여기서는 처리하지 않음

    def draw(self):
        frame_num = int(self.Player2.frame)
        if self.Player2.face_dir == 1:  # right
            self.Player2.image.clip_composite_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                                   int(pokemon.gengar_data['sprites'][frame_num]['height']), 0,
                                                   'h', self.Player2.x,
                                                   self.Player2.y, 100,
                                                   100)
        else:  # face_dir == -1: # left
            self.Player2.image.clip_draw(int(pokemon.gengar_data['sprites'][frame_num]["x"]),
                                         int(pokemon.gengar_data['sprites'][frame_num]['y']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['width']),
                                         int(pokemon.gengar_data['sprites'][frame_num]['height']), self.Player2.x,
                                         self.Player2.y, 100,
                                         100)



class Player2:
    def __init__(self):
        self.mycharacter = pokemon.Gengar()
        self.x, self.y = 1200, 90
        self.frame = 0
        self.face_dir = -1
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
                self.IDLE: {up_down: self.JUMP, down_down: self.DEFENSE, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN: {up_down: self.JUMP, down_down: self.DEFENSE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
                self.JUMP: {},
                self.DEFENSE: {down_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
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
        # if group == 'Player2:ball':
        #     self.ball_count += 1
        # if group == 'Player2:zombie':
        #     game_framework.quit()
        pass
