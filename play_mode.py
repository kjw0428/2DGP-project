import random
from pico2d import *

import game_framework
import game_world

from player1 import Player1
from player2 import Player2
from background import Ground

player1 = None
player2 = None
ground = None

# 라운드 타이머 (초)
ROUND_TIME = 60.0
round_time_remaining = ROUND_TIME

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.handle_event(event)
            player2.handle_event(event)

def init():
    global player1
    global player2
    global ground
    global round_time_remaining

    # 타이머 초기화
    round_time_remaining = ROUND_TIME

    # 배경을 먼저 생성해 레이어 0에 추가
    ground = Ground()
    game_world.add_object(ground, 0)

    # grass = Grass()
    # game_world.add_object(grass, 0)
    # game_world.add_collision_pair('grass:ball', grass, None)

    player1 = Player1()
    game_world.add_object(player1, 1)
    player2 = Player2()
    game_world.add_object(player2, 1)

    # player1과 player2의 충돌을 검사하도록 페어 등록
    game_world.add_collision_pair('player1:player2', player1, player2)

    # game_world.add_collision_pair('boy:ball',boy,None)
    # for ball in balls:
    #     game_world.add_collision_pair('boy:ball',None, ball)
    #
    # zombies = [Zombie() for _ in range(4)]
    # game_world.add_objects(zombies, 1)
    #
    # game_world.add_collision_pair('boy:zombie', boy, None)
    # for z in zombies:
    #     game_world.add_collision_pair('boy:zombie', None, z)
    #     game_world.add_collision_pair('ball:zombie', None, z)
def update():
    global round_time_remaining
    # 게임 월드 업데이트
    game_world.update()
    game_world.handle_collisions()

    # 타이머 감소(카운트다운). 게임 프레임 시간을 사용
    try:
        dt = game_framework.frame_time
    except Exception:
        dt = 0
    round_time_remaining -= dt

    # 플레이어 존재 확인 및 HP 종료 조건 검사
    try:
        p1_hp = player1.hp if player1 is not None else None
        p2_hp = player2.hp if player2 is not None else None
    except Exception:
        p1_hp = None
        p2_hp = None

    # 타이머 종료 시 종료
    if round_time_remaining <= 0:
        print('Time up. Exiting game.')
        game_framework.quit()
        return

    # 플레이어 HP가 0 이하이면 즉시 종료 (존재하는 플레이어만 검사)
    if p1_hp is not None and p1_hp <= 0:
        print('Player1 HP depleted. Player2 wins. Exiting game.')
        game_framework.quit()
        return
    if p2_hp is not None and p2_hp <= 0:
        print('Player2 HP depleted. Player1 wins. Exiting game.')
        game_framework.quit()
        return


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass