import pygame
import random

pygame.init()

# =========================
# TELA
# =========================

WIDTH = 800
HEIGHT = 600

# =========================
# CORES
# =========================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SIDEWALK = (210, 210, 210)
ROAD = (45, 45, 45)

GREEN = (40, 180, 40)
DARK_GREEN = (20, 130, 20)

BLUE = (50, 90, 220)

RED = (230, 40, 40)

SKY = (120, 190, 255)

GRAY = (140, 140, 140)
DARK_GRAY = (90, 90, 90)

YELLOW = (255, 225, 70)

# =========================
# PLAYER
# =========================

player = pygame.Rect(40, 500, 26, 42)

player_speed = 5

# =========================
# ITENS
# =========================

vertical_item = pygame.Rect(120, 430, 40, 40)

horizontal_item = pygame.Rect(640, 500, 40, 40)

has_vertical = False
has_horizontal = False

# =========================
# RUAS
# =========================

vertical_road = pygame.Rect(320, 0, 160, HEIGHT)

horizontal_road = pygame.Rect(0, 220, WIDTH, 160)

# =========================
# FAIXAS
# =========================

vertical_crosswalk_rect = pygame.Rect(
    325,
    410,
    150,
    70
)

horizontal_crosswalk_rect = pygame.Rect(
    250,
    225,
    70,
    150
)

# =========================
# SEMÁFORO
# =========================

signal_timer = 0

vertical_signal = "GREEN"

# =========================
# CARROS VERTICAIS
# =========================

vertical_cars = []

for i in range(3):

    vertical_cars.append(
        pygame.Rect(
            365,
            random.randint(-600, -50),
            45,
            80
        )
    )

# =========================
# CARROS HORIZONTAIS
# =========================

horizontal_cars = []

for i in range(3):

    horizontal_cars.append(
        pygame.Rect(
            random.randint(-900, -100),
            285,
            80,
            45
        )
    )

vertical_speed = 5
horizontal_speed = 5

# =========================
# ÁRVORES
# =========================

trees = [
    pygame.Rect(80, 120, 70, 70),
    pygame.Rect(670, 120, 70, 70),
    pygame.Rect(710, 430, 70, 70),
    pygame.Rect(120, 470, 70, 70),
]

# =========================
# RESET
# =========================

def reset_game():

    global has_vertical
    global has_horizontal

    player.x = 40
    player.y = 500

    has_vertical = False
    has_horizontal = False

    for car in vertical_cars:
        car.y = random.randint(-600, -50)

    for car in horizontal_cars:
        car.x = random.randint(-900, -100)

# =========================
# PLAYER
# =========================

def draw_player(screen):

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
# ÁRVORE
# =========================

def draw_tree(screen, rect):

    pygame.draw.ellipse(
        screen,
        (50, 50, 50),
        (rect.x + 8, rect.y + 50, 50, 18)
    )

    pygame.draw.rect(
        screen,
        (120, 70, 20),
        (rect.x + 28, rect.y + 35, 14, 35)
    )

    pygame.draw.circle(
        screen,
        DARK_GREEN,
        (rect.x + 28, rect.y + 30),
        26
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (rect.x + 42, rect.y + 28),
        22
    )

# =========================
# CARRO VERTICAL
# =========================

def draw_vertical_car(screen, car):

    pygame.draw.rect(
        screen,
        RED,
        car,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (180, 220, 255),
        (car.x + 6, car.y + 8, 33, 18),
        border_radius=5
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (car.x + 8, car.y + 70),
        5
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (car.x + 37, car.y + 70),
        5
    )

# =========================
# CARRO HORIZONTAL
# =========================

def draw_horizontal_car(screen, car):

    pygame.draw.rect(
        screen,
        BLUE,
        car,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (180, 220, 255),
        (car.x + 10, car.y + 6, 25, 30),
        border_radius=5
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (car.x + 15, car.y + 42),
        5
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (car.x + 65, car.y + 42),
        5
    )

# =========================
# SEMÁFORO
# =========================

def draw_traffic_light(screen, x, y, color):

    pygame.draw.rect(
        screen,
        BLACK,
        (x, y, 20, 60),
        border_radius=5
    )

    pygame.draw.circle(
        screen,
        color,
        (x + 10, y + 30),
        10
    )

# =========================
# GAME
# =========================

def run_phase2(screen):

    global has_vertical
    global has_horizontal
    global signal_timer
    global vertical_signal

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
    # USAR ITEM COM E
    # =========================

    near_vertical = player.colliderect(vertical_item)

    near_horizontal = player.colliderect(horizontal_item)

    if near_vertical and keys[pygame.K_e]:
        has_vertical = True

    if near_horizontal and keys[pygame.K_e]:
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
    # COLISÃO RUAS
    # =========================

    touching_vertical_road = player.colliderect(
        vertical_road.inflate(-40, 0)
    )

    touching_horizontal_road = player.colliderect(
        horizontal_road.inflate(0, -40)
    )

    on_vertical_crosswalk = player.colliderect(
        vertical_crosswalk_rect
    )

    on_horizontal_crosswalk = player.colliderect(
        horizontal_crosswalk_rect
    )

    if touching_vertical_road:

        if not on_vertical_crosswalk:

            txt_font = pygame.font.SysFont(
                "Arial",
                45,
                bold=True
            )

            txt = txt_font.render(
                "USE A FAIXA!",
                True,
                RED
            )

            screen.blit(txt, (220, 260))

            pygame.display.update()

            pygame.time.delay(1200)

            reset_game()

    if touching_horizontal_road:

        if not on_horizontal_crosswalk:

            txt_font = pygame.font.SysFont(
                "Arial",
                45,
                bold=True
            )

            txt = txt_font.render(
                "USE A FAIXA!",
                True,
                RED
            )

            screen.blit(txt, (220, 260))

            pygame.display.update()

            pygame.time.delay(1200)

            reset_game()

    # =========================
    # CARROS VERTICAIS
    # =========================

    for car in vertical_cars:

        if vertical_signal == "GREEN":
            car.y += vertical_speed

        if car.y > HEIGHT:
            car.y = random.randint(-500, -100)

        if player.colliderect(car):
            reset_game()

    # =========================
    # CARROS HORIZONTAIS
    # =========================

    for car in horizontal_cars:

        if vertical_signal == "RED":
            car.x += horizontal_speed

        if car.x > WIDTH:
            car.x = random.randint(-700, -100)

        if player.colliderect(car):
            reset_game()

    # =========================
    # CENÁRIO
    # =========================

    screen.fill(SIDEWALK)

    pygame.draw.rect(screen, SKY, (0, 0, WIDTH, 90))

    pygame.draw.circle(screen, YELLOW, (670, 45), 30)

    pygame.draw.circle(screen, WHITE, (470, 40), 25)
    pygame.draw.circle(screen, WHITE, (500, 40), 30)
    pygame.draw.circle(screen, WHITE, (530, 40), 25)

    # GRID
    for x in range(0, WIDTH, 30):
        pygame.draw.line(screen, (190, 190, 190), (x, 90), (x, HEIGHT))

    for y in range(90, HEIGHT, 30):
        pygame.draw.line(screen, (190, 190, 190), (0, y), (WIDTH, y))

    # RUAS
    pygame.draw.rect(screen, ROAD, vertical_road)

    pygame.draw.rect(screen, ROAD, horizontal_road)

    # LINHAS VERTICAIS
    for y in range(0, HEIGHT, 90):

        pygame.draw.rect(
            screen,
            WHITE,
            (392, y, 16, 50),
            border_radius=5
        )

    # LINHAS HORIZONTAIS
    for x in range(0, WIDTH, 90):

        pygame.draw.rect(
            screen,
            WHITE,
            (x, 292, 50, 16),
            border_radius=5
        )

    # =========================
    # FAIXA VERTICAL
    # =========================

    if has_vertical:

        for i in range(6):

            pygame.draw.rect(
                screen,
                WHITE,
                (
                    325 + i * 25,
                    420,
                    16,
                    50
                ),
                border_radius=3
            )

    # =========================
    # FAIXA HORIZONTAL
    # =========================

    if has_horizontal:

        for i in range(6):

            pygame.draw.rect(
                screen,
                WHITE,
                (
                    260,
                    230 + i * 22,
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

    screen.blit(txt, (625, 70))

    # =========================
    # SEMÁFOROS
    # =========================

    vertical_color = GREEN if vertical_signal == "GREEN" else RED

    horizontal_color = RED if vertical_signal == "GREEN" else GREEN

    # semáforo carros vertical
    draw_traffic_light(
        screen,
        500,
        180,
        vertical_color
    )

    # semáforo carros horizontal
    draw_traffic_light(
        screen,
        270,
        390,
        horizontal_color
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
                (125, y),
                (155, y),
                3
            )

        item_font = pygame.font.SysFont(
            "Arial",
            20,
            bold=True
        )

        txt = item_font.render(
            "Faixa V",
            True,
            BLACK
        )

        screen.blit(txt, (90, 475))

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

        item_font = pygame.font.SysFont(
            "Arial",
            20,
            bold=True
        )

        txt = item_font.render(
            "Faixa H",
            True,
            BLACK
        )

        screen.blit(txt, (610, 548))

    # =========================
    # APERTE E
    # =========================

    hint_font = pygame.font.SysFont(
        "Arial",
        22,
        bold=True
    )

    if near_vertical and not has_vertical:

        txt = hint_font.render(
            "APERTE E",
            True,
            BLACK
        )

        screen.blit(txt, (70, 390))

    if near_horizontal and not has_horizontal:

        txt = hint_font.render(
            "APERTE E",
            True,
            BLACK
        )

        screen.blit(txt, (610, 465))

    # =========================
    # CARROS
    # =========================

    for car in vertical_cars:
        draw_vertical_car(screen, car)

    for car in horizontal_cars:
        draw_horizontal_car(screen, car)

    # =========================
    # PLAYER
    # =========================

    draw_player(screen)

    # =========================
    # HUD
    # =========================

    hud = pygame.Rect(10, 10, 360, 140)

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        hud,
        border_radius=12
    )

    hud_font = pygame.font.SysFont(
        "Arial",
        24,
        bold=True
    )

    vertical_text = hud_font.render(
        f"Faixa Vertical: {'SIM' if has_vertical else 'NAO'}",
        True,
        BLACK
    )

    horizontal_text = hud_font.render(
        f"Faixa Horizontal: {'SIM' if has_horizontal else 'NAO'}",
        True,
        BLACK
    )

    signal_text = hud_font.render(
        f"Sinal Vertical: {vertical_signal}",
        True,
        BLACK
    )

    screen.blit(vertical_text, (20, 25))

    screen.blit(horizontal_text, (20, 60))

    screen.blit(signal_text, (20, 95))

    # =========================
    # VITÓRIA
    # =========================

    school_area = pygame.Rect(590, 40, 170, 190)

    if player.colliderect(school_area):

        if has_vertical and has_horizontal:

            overlay = pygame.Surface((WIDTH, HEIGHT))

            overlay.set_alpha(210)

            overlay.fill((0, 0, 0))

            screen.blit(overlay, (0, 0))

            pygame.draw.rect(
                screen,
                WHITE,
                (90, 170, 620, 220),
                border_radius=20
            )

            victory_font = pygame.font.SysFont(
                "Arial",
                34,
                bold=True
            )

            small_font = pygame.font.SysFont(
                "Arial",
                26
            )

            title = victory_font.render(
                "VOCÊ CHEGOU À ESCOLA!",
                True,
                GREEN
            )

            desc = small_font.render(
                "Atravessar corretamente salva vidas.",
                True,
                BLACK
            )

            screen.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    245
                )
            )

            screen.blit(
                desc,
                (
                    WIDTH // 2 - desc.get_width() // 2,
                    315
                )
            )

            pygame.display.update()

            pygame.time.delay(1800)

            return "menu"