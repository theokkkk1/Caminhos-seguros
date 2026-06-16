# =========================
# PHASE 2
# =========================

import pygame

from screens.phase1 import (
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK,
    SIDEWALK,
    ROAD,
    GREEN,
    BLUE,
    RED,
    SKY,
    DARK_GRAY,
    YELLOW,
    draw_tree,
    draw_car
)

def run_phase2(screen):

    clock = pygame.time.Clock()

    # =========================
    # PLAYER
    # =========================

    player = pygame.Rect(120, 500, 26, 42)

    player_speed = 4

    # =========================
    # ITENS DAS FAIXAS
    # =========================

    vertical_item = pygame.Rect(110, 430, 40, 40)

    horizontal_item = pygame.Rect(640, 500, 40, 40)

    has_vertical = False
    has_horizontal = False

    # =========================
    # RUAS
    # =========================

    vertical_road = pygame.Rect(
        320,
        0,
        160,
        HEIGHT
    )

    horizontal_road = pygame.Rect(
        0,
        240,
        WIDTH,
        160
    )

    # =========================
    # FAIXAS
    # =========================

    vertical_crosswalk = pygame.Rect(
        320,
        420,
        160,
        70
    )

    horizontal_crosswalk = pygame.Rect(
        480,
        240,
        70,
        160
    )

    # =========================
    # SISTEMA DE CARROS
    # =========================

    vertical_lane_x = 365
    horizontal_lane_y = 295

    # velocidade aumentada
    vertical_speed = 4
    horizontal_speed = 4

    vertical_cars = []
    horizontal_cars = []

    # carros verticais
    for i in range(3):

        car = pygame.Rect(
            vertical_lane_x,
            -250 * i - 120,
            45,
            80
        )

        vertical_cars.append(car)

    # carros horizontais
    for i in range(3):

        car = pygame.Rect(
            -320 * i - 200,
            horizontal_lane_y,
            80,
            45
        )

        horizontal_cars.append(car)

    # =========================
    # SEMÁFORO
    # =========================

    signal_timer = 0
    vertical_signal = "GREEN"

    # =========================
    # ÁRVORES
    # =========================

    trees = [
        pygame.Rect(70, 120, 70, 70),
        pygame.Rect(660, 120, 70, 70),
        pygame.Rect(680, 460, 70, 70),
    ]

    # =========================
    # RESET
    # =========================

    def reset_game():

        nonlocal has_vertical
        nonlocal has_horizontal

        player.x = 120
        player.y = 500

        has_vertical = False
        has_horizontal = False

    # =========================
    # LOOP PRINCIPAL
    # =========================

    while True:

        clock.tick(60)

        # =========================
        # EVENTOS
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "menu"

        keys = pygame.key.get_pressed()

        old_x = player.x
        old_y = player.y

        # =========================
        # MOVIMENTO
        # =========================

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        # =========================
        # LIMITES
        # =========================

        if player.x < 0:
            player.x = 0

        if player.x > WIDTH - player.width:
            player.x = WIDTH - player.width

        if player.y < 0:
            player.y = 0

        if player.y > HEIGHT - player.height:
            player.y = HEIGHT - player.height

        # =========================
        # COLISÃO ÁRVORES
        # =========================

        for tree in trees:

            if player.colliderect(tree):

                player.x = old_x
                player.y = old_y

        # =========================
        # PEGAR FAIXAS
        # =========================

        if player.colliderect(vertical_item):

            if keys[pygame.K_e]:
                has_vertical = True

        if player.colliderect(horizontal_item):

            if keys[pygame.K_e]:
                has_horizontal = True

        # =========================
        # SEMÁFORO
        # =========================

        signal_timer += 1

        if signal_timer < 240:
            vertical_signal = "GREEN"
        else:
            vertical_signal = "RED"

        if signal_timer > 480:
            signal_timer = 0

        # =========================
        # COLISÃO COM RUAS
        # =========================

        touching_vertical = player.colliderect(
            vertical_road.inflate(-40, 0)
        )

        touching_horizontal = player.colliderect(
            horizontal_road.inflate(0, -40)
        )

        on_vertical_crosswalk = player.colliderect(
            vertical_crosswalk
        )

        on_horizontal_crosswalk = player.colliderect(
            horizontal_crosswalk
        )

        # =========================
        # AVISO DE FAIXA
        # =========================

        invalid_cross = False

        if touching_vertical and not on_vertical_crosswalk:
            invalid_cross = True

        if touching_horizontal and not on_horizontal_crosswalk:
            invalid_cross = True

        if invalid_cross:

            warning_font = pygame.font.SysFont(
                "Arial",
                42,
                bold=True
            )

            warning_text = warning_font.render(
                "USE A FAIXA!",
                True,
                RED
            )

            screen.blit(
                warning_text,
                (
                    WIDTH // 2 - warning_text.get_width() // 2,
                    180
                )
            )

            pygame.display.update()

            pygame.time.delay(1000)

            reset_game()

        # =========================
        # ATUALIZAÇÃO DOS CARROS
        # =========================

        vertical_cars.sort(key=lambda c: c.y)

        for i, car in enumerate(vertical_cars):

            move = True

            stop_line = 215

            if vertical_signal == "RED":

                if car.y + car.height >= stop_line:
                    move = False

            if i > 0:

                front = vertical_cars[i - 1]

                distance = front.y - (car.y + car.height)

                if distance < 110:
                    move = False

            if move:
                car.y += vertical_speed

            if car.y > HEIGHT + 150:

                top_y = min(c.y for c in vertical_cars)

                car.y = top_y - 300

            hitbox = car.inflate(-12, -12)

            if player.colliderect(hitbox):

                reset_game()

        horizontal_cars.sort(key=lambda c: c.x)

        for i, car in enumerate(horizontal_cars):

            move = True

            stop_line = 305

            if vertical_signal == "GREEN":

                if car.x + car.width >= stop_line:
                    move = False

            if i > 0:

                front = horizontal_cars[i - 1]

                distance = front.x - (car.x + car.width)

                if distance < 140:
                    move = False

            if move:
                car.x += horizontal_speed

            if car.x > WIDTH + 180:

                left_x = min(c.x for c in horizontal_cars)

                car.x = left_x - 360

            hitbox = car.inflate(-12, -12)

            if player.colliderect(hitbox):

                reset_game()

        # =========================
        # CENÁRIO
        # =========================

        screen.fill(SIDEWALK)

        pygame.draw.rect(
            screen,
            SKY,
            (0, 0, WIDTH, 90)
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (670, 45),
            30
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (470, 40),
            25
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (500, 40),
            30
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (530, 40),
            25
        )

        # chão

        for x in range(0, WIDTH, 30):

            pygame.draw.line(
                screen,
                (190, 190, 190),
                (x, 90),
                (x, HEIGHT)
            )

        for y in range(90, HEIGHT, 30):

            pygame.draw.line(
                screen,
                (190, 190, 190),
                (0, y),
                (WIDTH, y)
            )

        # ruas

        pygame.draw.rect(
            screen,
            ROAD,
            vertical_road
        )

        pygame.draw.rect(
            screen,
            ROAD,
            horizontal_road
        )

        # linhas

        for y in range(0, HEIGHT, 90):

            pygame.draw.rect(
                screen,
                WHITE,
                (392, y, 16, 50),
                border_radius=5
            )

        for x in range(0, WIDTH, 90):

            pygame.draw.rect(
                screen,
                WHITE,
                (x, 312, 50, 16),
                border_radius=5
            )

        # =========================
        # FAIXAS
        # =========================

        if has_vertical:

            for i in range(6):

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        326 + i * 24,
                        430,
                        16,
                        50
                    ),
                    border_radius=3
                )

        if has_horizontal:

            for i in range(6):

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        490,
                        248 + i * 24,
                        50,
                        16
                    ),
                    border_radius=3
                )

        # =========================
        # ÁRVORES
        # =========================

        for tree in trees:
            draw_tree(screen, tree)

        # =========================
        # ESCOLA
        # =========================

        pygame.draw.rect(
            screen,
            (245, 210, 120),
            (600, 90, 140, 130),
            border_radius=12
        )

        pygame.draw.polygon(
            screen,
            RED,
            [
                (590, 100),
                (670, 40),
                (750, 100)
            ]
        )

        pygame.draw.rect(
            screen,
            DARK_GRAY,
            (655, 165, 30, 55),
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            (180, 220, 255),
            (620, 120, 24, 24),
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            (180, 220, 255),
            (695, 120, 24, 24),
            border_radius=4
        )

        school_font = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )

        txt = school_font.render(
            "ESCOLA",
            True,
            BLACK
        )

        screen.blit(txt, (620, 70))

        # =========================
        # SEMÁFOROS
        # =========================

        vertical_color = GREEN if vertical_signal == "GREEN" else RED

        horizontal_color = RED if vertical_signal == "GREEN" else GREEN

        pygame.draw.rect(
            screen,
            BLACK,
            (500, 180, 20, 60),
            border_radius=5
        )

        pygame.draw.circle(
            screen,
            vertical_color,
            (510, 210),
            10
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (260, 390, 20, 60),
            border_radius=5
        )

        pygame.draw.circle(
            screen,
            horizontal_color,
            (270, 420),
            10
        )

        # =========================
        # ITENS
        # =========================

        if not has_vertical:

            pygame.draw.rect(
                screen,
                WHITE,
                vertical_item,
                border_radius=4
            )

            for y in range(435, 465, 6):

                pygame.draw.line(
                    screen,
                    BLACK,
                    (115, y),
                    (145, y),
                    3
                )

        if not has_horizontal:

            pygame.draw.rect(
                screen,
                WHITE,
                horizontal_item,
                border_radius=4
            )

            for x in range(645, 675, 6):

                pygame.draw.line(
                    screen,
                    BLACK,
                    (x, 505),
                    (x, 535),
                    3
                )

        # =========================
        # CARROS VERTICAIS
        # =========================

        for car in vertical_cars:

            pygame.draw.rect(
                screen,
                (220, 60, 60),
                car,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                (180, 220, 255),
                (
                    car.x + 7,
                    car.y + 10,
                    30,
                    18
                ),
                border_radius=4
            )

        # =========================
        # CARROS HORIZONTAIS
        # =========================

        for car in horizontal_cars:

            pygame.draw.rect(
                screen,
                (60, 120, 255),
                car,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                (180, 220, 255),
                (
                    car.x + 10,
                    car.y + 7,
                    22,
                    28
                ),
                border_radius=4
            )

        # =========================
        # PLAYER
        # =========================

        pygame.draw.circle(
            screen,
            (255, 220, 180),
            (player.x + 13, player.y + 10),
            10
        )

        pygame.draw.rect(
            screen,
            BLUE,
            (player.x + 4, player.y + 18, 18, 22),
            border_radius=5
        )

        pygame.draw.line(
            screen,
            BLACK,
            (player.x + 8, player.y + 40),
            (player.x + 4, player.y + 50),
            3
        )

        pygame.draw.line(
            screen,
            BLACK,
            (player.x + 18, player.y + 40),
            (player.x + 22, player.y + 50),
            3
        )

        pygame.draw.line(
            screen,
            BLACK,
            (player.x + 4, player.y + 28),
            (player.x - 2, player.y + 36),
            3
        )

        pygame.draw.line(
            screen,
            BLACK,
            (player.x + 22, player.y + 28),
            (player.x + 28, player.y + 36),
            3
        )

        # =========================
        # VITÓRIA
        # =========================

        school_area = pygame.Rect(
            590,
            40,
            170,
            190
        )

        if player.colliderect(school_area):

            if has_vertical and has_horizontal:

                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))

                screen.blit(overlay, (0, 0))

                victory_font = pygame.font.SysFont(
                    "Arial",
                    40,
                    bold=True
                )

                small_font = pygame.font.SysFont(
                    "Arial",
                    26
                )

                victory_text = victory_font.render(
                    "VOCÊ CHEGOU À ESCOLA!",
                    True,
                    GREEN
                )

                info_text = small_font.render(
                    "Parabéns por atravessar com segurança.",
                    True,
                    WHITE
                )

                screen.blit(
                    victory_text,
                    (
                        WIDTH // 2 - victory_text.get_width() // 2,
                        240
                    )
                )

                screen.blit(
                    info_text,
                    (
                        WIDTH // 2 - info_text.get_width() // 2,
                        300
                    )
                )

                pygame.display.update()

                pygame.time.delay(1500)

                return "phase3"

        pygame.display.update()

        
        