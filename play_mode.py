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
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
