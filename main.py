from pico2d import open_canvas, delay, close_canvas, load_image, clear_canvas, update_canvas, get_events, SDL_KEYDOWN
import game_framework

import play_mode as start_mode

def show_start_screen():
    start_image = load_image('start1.png')
    canvas_width, canvas_height = 1200, 600  # 캔버스 크기
    while True:
        clear_canvas()
        start_image.draw(canvas_width // 2, canvas_height // 2, canvas_width, canvas_height)  # 캔버스 크기에 맞게 이미지 출력
        update_canvas()
        events = get_events()
        for event in events:
            if event.type == SDL_KEYDOWN:  # 키 입력이 발생하면 시작
                return

open_canvas(1200, 600)
show_start_screen()  # 시작 화면 표시
game_framework.run(start_mode)
close_canvas()