from pico2d import load_image, get_canvas_width, get_canvas_height

class Ground:
    def __init__(self):
        self.image = load_image('background1.png')

    def update(self):
        pass

    def draw(self):
        # 현재 캔버스 크기를 읽어와 중앙에 캔버스 크기로 스케일하여 그림
        w = get_canvas_width()
        h = get_canvas_height()
        self.image.draw(w // 2, h // 2, w, h)
