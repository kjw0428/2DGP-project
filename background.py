from pico2d import load_image, get_canvas_width, get_canvas_height, get_time
import json
import game_world

class Ground:
    def __init__(self):
        # 배경 이미지
        try:
            self.image = load_image('background1.png')
        except Exception:
            self.image = None

        # hp-bar 스프라이트 이미지와 메타데이터 로드
        try:
            self.hp_image = load_image('hp-bar.png')
        except Exception:
            self.hp_image = None
            self.hp_sprite0 = None
            self.hp_sprite8 = None
            return

        try:
            with open('hp-bar_data.json', 'r', encoding='utf-8') as f:
                raw = f.read()
                raw = '\n'.join([line for line in raw.splitlines() if not line.strip().startswith('//')])
                data = json.loads(raw)
            sprites = {s['name']: s for s in data['sprites']}
            self.hp_sprite0 = sprites.get('hp-bar_0')
            self.hp_sprite8 = sprites.get('hp-bar_8')
        except Exception:
            self.hp_sprite0 = None
            self.hp_sprite8 = None

        # number 스프라이트(카운트다운) 로드
        try:
            self.number_image = load_image('number.png')
        except Exception:
            self.number_image = None
            self.number_sprites = None
            # 타이머 시작 시간
            self.start_time = get_time()
            return

        try:
            with open('number_data.json', 'r', encoding='utf-8') as f:
                raw = f.read()
                raw = '\n'.join([line for line in raw.splitlines() if not line.strip().startswith('//')])
                data = json.loads(raw)
            # sprites를 인덱스별로 정렬하여 리스트로 보관 (number_0 ... number_9)
            sprites = {s['name']: s for s in data['sprites']}
            self.number_sprites = [sprites.get(f'number_{i}') for i in range(10)]
        except Exception:
            self.number_sprites = None

        # 카운트다운 시작 시간(초)
        self.start_time = get_time()

    def update(self):
        # 남은 시간 계산(정수 초 단위)
        try:
            elapsed = get_time() - self.start_time
            self.remaining_seconds = max(0, 60 - int(elapsed))
        except Exception:
            self.remaining_seconds = 0

    def draw(self):
        w = get_canvas_width()
        h = get_canvas_height()

        # 배경 그리기
        if self.image:
            try:
                self.image.draw(w // 2, h // 2, w, h)
            except Exception:
                pass

        # hp 관련 리소스가 준비되지 않았으면 종료
        if not (self.hp_image and self.hp_sprite0 and self.hp_sprite8):
            return

        # 소스 정보
        sx0 = int(self.hp_sprite0['x'])
        sy0 = int(self.hp_sprite0['y'])
        sw0 = int(self.hp_sprite0['width'])
        sh0 = int(self.hp_sprite0['height'])

        sx8 = int(self.hp_sprite8['x'])
        sy8 = int(self.hp_sprite8['y'])
        sw8 = int(self.hp_sprite8['width'])
        sh8 = int(self.hp_sprite8['height'])

        # 축소 비율과 목표 크기
        scale = 0.6
        dest_w_full = max(1, int(sw0 * scale))
        dest_h = max(1, int(sh0 * scale))
        margin = 20

        # game_world에서 hp와 x 속성 가진 객체 수집
        players = []
        for layer in game_world.world:
            for o in layer:
                if hasattr(o, 'hp') and hasattr(o, 'x'):
                    players.append(o)

        # 좌/우 그릴 영역의 왼쪽 x 좌표(픽셀)
        left_dest_left = margin
        right_dest_left = w - margin - dest_w_full
        top_y = h - margin - (dest_h // 2)

        # clip_draw 시 y축 기준이 달라 예외가 날 경우를 대비한 보정 함수
        def try_clip_draw(img, sx, sy, sw, sh, dx, dy, dw, dh):
            try:
                img.clip_draw(sx, sy, sw, sh, dx, dy, dw, dh)
            except Exception:
                try:
                    img_h = img.h
                    flipped_sy = img_h - (sy + sh)
                    img.clip_draw(sx, flipped_sy, sw, sh, dx, dy, dw, dh)
                except Exception:
                    pass

        # 플레이어가 2명 미만이면 전체 바 이미지를 좌/우에 그대로 그림
        if len(players) < 2:
            left_cx = left_dest_left + dest_w_full // 2
            right_cx = right_dest_left + dest_w_full // 2
            try_clip_draw(self.hp_image, sx8, sy8, sw8, sh8, left_cx, top_y, dest_w_full, dest_h)
            try_clip_draw(self.hp_image, sx0, sy0, sw0, sh0, left_cx, top_y, dest_w_full, dest_h)
            try_clip_draw(self.hp_image, sx8, sy8, sw8, sh8, right_cx, top_y, dest_w_full, dest_h)
            try_clip_draw(self.hp_image, sx0, sy0, sw0, sh0, right_cx, top_y, dest_w_full, dest_h)

            # 플레이어가 2명 미만일 때도 중앙에 타이머 표시
            if self.number_image and self.number_sprites:
                sec = getattr(self, 'remaining_seconds', max(0, 60 - int(get_time() - self.start_time)))
                tens = sec // 10
                units = sec % 10
                # 숫자 스프라이트 정보
                ts = self.number_sprites[tens]
                us = self.number_sprites[units]
                if ts and us:
                    # 숫자 크기 조정
                    num_scale = 1.2
                    tw = int(ts['width'] * num_scale)
                    th = int(ts['height'] * num_scale)
                    ux = int(us['width'] * num_scale)
                    # 중심 위치
                    center_x = (left_cx + right_cx) // 2
                    # 두 숫자를 좌우로 배치
                    try_clip_draw(self.number_image, int(ts['x']), int(ts['y']), int(ts['width']), int(ts['height']), center_x - tw//2, top_y, tw, th)
                    try_clip_draw(self.number_image, int(us['x']), int(us['y']), int(us['width']), int(us['height']), center_x + ux//2, top_y, ux, th)
            return

        # 왼쪽/오른쪽 플레이어 선택
        left_player = min(players, key=lambda p: p.x)
        right_player = max(players, key=lambda p: p.x)

        # 왼쪽 바 그리기: 먼저 빈 부분(hp-bar_8) 전체를 그리고, 그 위에 채워진 부분(hp-bar_0)을 왼쪽 정렬로 오버레이
        def draw_for_left(hp):
            hp_ratio = max(0.0, min(1.0, hp / 100.0))
            # 빈 부분 전체 (먼저 그림)
            left_cx = left_dest_left + dest_w_full // 2
            try_clip_draw(self.hp_image, sx8, sy8, sw8, sh8, left_cx, top_y, dest_w_full, dest_h)

            # 채워진 부분을 오버레이
            if hp_ratio > 0:
                src_w0 = max(1, int(sw0 * hp_ratio))
                dest_w = max(1, int(dest_w_full * hp_ratio))
                src_x = sx0
                dest_cx_filled = left_dest_left + dest_w // 2
                try_clip_draw(self.hp_image, src_x, sy0, src_w0, sh0, dest_cx_filled, top_y, dest_w, dest_h)

        # 오른쪽 바 그리기: 먼저 빈 부분(hp-bar_8) 전체를 그리고, 그 위에 채워진 부분(hp-bar_0)을 오른쪽 정렬로 오버레이
        def draw_for_right(hp):
            hp_ratio = max(0.0, min(1.0, hp / 100.0))
            right_cx = right_dest_left + dest_w_full // 2
            try_clip_draw(self.hp_image, sx8, sy8, sw8, sh8, right_cx, top_y, dest_w_full, dest_h)

            if hp_ratio > 0:
                src_w0 = max(1, int(sw0 * hp_ratio))
                dest_w = max(1, int(dest_w_full * hp_ratio))
                src_x = sx0 + (sw0 - src_w0)
                dest_cx_filled = right_dest_left + dest_w_full - (dest_w // 2)
                try_clip_draw(self.hp_image, src_x, sy0, src_w0, sh0, dest_cx_filled, top_y, dest_w, dest_h)

        draw_for_left(getattr(left_player, 'hp', 0))
        draw_for_right(getattr(right_player, 'hp', 0))

        # 타이머 그리기 (플레이어 2명 이상일 때 중앙에 표시)
        if self.number_image and self.number_sprites:
            sec = getattr(self, 'remaining_seconds', max(0, 60 - int(get_time() - self.start_time)))
            tens = sec // 10
            units = sec % 10
            ts = self.number_sprites[tens]
            us = self.number_sprites[units]
            if ts and us:
                # 숫자 크기 및 위치 계산
                num_scale = 1.2
                tw = int(ts['width'] * num_scale)
                th = int(ts['height'] * num_scale)
                uw = int(us['width'] * num_scale)
                left_cx = left_dest_left + dest_w_full // 2
                right_cx = right_dest_left + dest_w_full // 2
                center_x = (left_cx + right_cx) // 2
                # 왼쪽(십의 자리), 오른쪽(일의 자리) 위치
                try_clip_draw(self.number_image, int(ts['x']), int(ts['y']), int(ts['width']), int(ts['height']), center_x - tw//2 - 8, top_y, tw, th)
                try_clip_draw(self.number_image, int(us['x']), int(us['y']), int(us['width']), int(us['height']), center_x + uw//2 - 8, top_y, uw, th)
