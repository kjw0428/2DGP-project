from pico2d import *
import game_framework
import game_world
import pygame  # 사운드 재생을 위한 pygame 추가

from player1 import Player1
from player2 import Player2
from background import Ground

player1 = None
player2 = None
ground = None

# 라운드 설정
ROUND_TIME = 60.0
MAX_ROUNDS = 3
WIN_REQUIRED = 2

# 상태 변수
round_time_remaining = ROUND_TIME
rounds_played = 0
p1_wins = 0
p2_wins = 0

def _end_match_and_quit(final_winner=None):
    global number_image

    # 결과 이미지 로드
    result_image = None
    if final_winner == 1:
        print('Match over. Player1 wins the match!')
        result_image = load_image('1pwin.png')
    elif final_winner == 2:
        print('Match over. Player2 wins the match!')
        result_image = load_image('2pwin.png')
    else:
        print('Match over. Draw.')
        result_image = load_image('draw.png')

    # 결과 이미지 출력
    if result_image:
        clear_canvas()
        result_image.draw(600, 300)  # 화면 중앙에 이미지 출력
        update_canvas()
        delay(3)  # 3초간 결과 화면 유지

    # 안전하게 프레임워크 종료 호출
    try:
        game_framework.quit()
    except Exception:
        pass


def _prepare_next_round():
    global round_time_remaining, player1, player2
    round_time_remaining = ROUND_TIME
    # 플레이어 상태 리셋(객체가 있으면)
    try:
        if player1 is not None:
            player1.hp = 100
            player1.x, player1.y = 300, 90
            player1.frame = 0
            player1.dir = 0
            player1.vy = 0.0
            player1.face_dir = 1
            try:
                player1.state_machine.cur_state = player1.IDLE
                player1.state_machine.cur_state.enter(('RESET', None))
            except Exception:
                pass
        if player2 is not None:
            player2.hp = 100
            player2.x, player2.y = 900, 90
            player2.frame = 0
            player2.dir = 0
            player2.vy = 0.0
            player2.face_dir = -1
            try:
                player2.state_machine.cur_state = player2.IDLE
                player2.state_machine.cur_state.enter(('RESET', None))
            except Exception:
                pass
    except Exception as e:
        print('Prepare next round error:', e)


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if player1:
                player1.handle_event(event)
            if player2:
                player2.handle_event(event)


def init():
    global player1, player2, ground, rounds_played, p1_wins, p2_wins, round_time_remaining

    # pygame 초기화 및 배경음악 로드
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.mixer.music.load('battle.mp3')
        pygame.mixer.music.set_volume(0.5)  # 볼륨 설정 (0.0 ~ 1.0)
        pygame.mixer.music.play(-1)  # 무한 반복 재생
    except Exception as e:
        print(f"Error loading or playing background music: {e}")

    rounds_played = 0
    p1_wins = 0
    p2_wins = 0
    round_time_remaining = ROUND_TIME

    ground = Ground()
    game_world.add_object(ground, 0)

    player1 = Player1()
    game_world.add_object(player1, 1)
    player2 = Player2()
    game_world.add_object(player2, 1)

    game_world.add_collision_pair('player1:player2', player1, player2)

    # 첫 라운드 준비
    _prepare_next_round()


def update():
    global round_time_remaining, rounds_played, p1_wins, p2_wins

    game_world.update()
    game_world.handle_collisions()

    try:
        dt = game_framework.frame_time
    except Exception:
        dt = 0
    round_time_remaining -= dt

    # 안전하게 HP 읽기
    try:
        p1_hp = player1.hp if player1 is not None else None
        p2_hp = player2.hp if player2 is not None else None
    except Exception:
        p1_hp = None
        p2_hp = None

    # 라운드 종료 판정
    round_end = False
    round_winner = None
    if p1_hp is not None and p1_hp <= 0:
        round_end = True
        round_winner = 2
    elif p2_hp is not None and p2_hp <= 0:
        round_end = True
        round_winner = 1
    elif round_time_remaining <= 0:
        round_end = True
        if p1_hp is not None and p2_hp is not None:
            if p1_hp > p2_hp:
                round_winner = 1
            elif p2_hp > p1_hp:
                round_winner = 2
            else:
                round_winner = 0
        else:
            round_winner = 0

    if round_end:
        rounds_played += 1
        if round_winner == 1:
            p1_wins += 1
            print(f'Round {rounds_played}: Player1 wins (score {p1_wins}:{p2_wins})')
        elif round_winner == 2:
            p2_wins += 1
            print(f'Round {rounds_played}: Player2 wins (score {p1_wins}:{p2_wins})')
        else:
            print(f'Round {rounds_played}: Draw (score {p1_wins}:{p2_wins})')

        # 매치 종료 검사
        if p1_wins >= WIN_REQUIRED or p2_wins >= WIN_REQUIRED or rounds_played >= MAX_ROUNDS:
            if p1_wins > p2_wins:
                final = 1
            elif p2_wins > p1_wins:
                final = 2
            else:
                final = 0
            _end_match_and_quit(final)
            return

        _prepare_next_round()
        return


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pygame.mixer.music.stop()  # 배경음악 정지
    pygame.quit()  # pygame 종료


def pause():
    pass


def resume():
    pass
