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

BLUE = (50, 90, 220)
RED = (230, 40, 40)

YELLOW = (255, 225, 70)

SKY = (120, 190, 255)

# =========================
# PLAYER
# =========================

player = pygame.Rect(80, 500, 26, 42)
player_speed = 4

# =========================
# HOSPITAL
# =========================

hospital = pygame.Rect(640, 60, 120, 120)

# =========================
# PISO TÁTIL
# =========================

tactile_path = [
    pygame.Rect(100, 520, 40, 20),
    pygame.Rect(140, 520, 40, 20),
    pygame.Rect(180, 520, 40, 20),
    pygame.Rect(220, 520, 40, 20),
    pygame.Rect(260, 520, 40, 20),
    pygame.Rect(300, 520, 40, 20),
    pygame.Rect(340, 520, 40, 20),

    pygame.Rect(360, 480, 20, 40),
    pygame.Rect(360, 440, 20, 40),
    pygame.Rect(360, 400, 20, 40),

    pygame.Rect(360, 360, 40, 20),
    pygame.Rect(400, 360, 40, 20),
    pygame.Rect(440, 360, 40, 20),
    pygame.Rect(480, 360, 40, 20),
    pygame.Rect(520, 360, 40, 20),

    pygame.Rect(560, 320, 20, 40),
    pygame.Rect(560, 280, 20, 40),
    pygame.Rect(560, 240, 20, 40),
]

# =========================
# RUA
# =========================

road = pygame.Rect(250, 200, 300, 160)

# =========================
# FAIXA DE PEDESTRE
# =========================

crosswalk = pygame.Rect(330, 200, 120, 160)

# =========================
# CARROS
# =========================

cars = []

for i in range(3):

    cars.append(
        pygame.Rect(
            random.randint(-500, -50),
            260,
            80,
            45
        )
    )

car_speed = 5

# =========================
# FONTE
# =========================

font = pygame.font.SysFont("Arial", 24, bold=True)

# =========================
# RESET
# =========================

def reset_game():

    player.x = 80
    player.y = 500

    for car in cars:
        car.x = random.randint(-500, -50)

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

# =========================
# CARRO
# =========================

def draw_car(screen, car):

    pygame.draw.rect(
        screen,
        RED,
        car,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (180, 220, 255),
        (car.x + 8, car.y + 8, 35, 18),
        border_radius=4
    )

    pygame.draw.circle(screen, BLACK, (car.x + 12, car.y + 40), 5)
    pygame.draw.circle(screen, BLACK, (car.x + 68, car.y + 40), 5)

# =========================
# HOSPITAL
# =========================

def draw_hospital(screen):

    pygame.draw.rect(
        screen,
        (235, 235, 235),
        hospital,
        border_radius=15
    )

    pygame.draw.rect(screen, RED, (690, 90, 20, 60))
    pygame.draw.rect(screen, RED, (670, 110, 60, 20))

# =========================
# VISÃO REDUZIDA
# =========================

def draw_vision_effect(screen):

    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    darkness.fill((0, 0, 0, 220))

    pygame.draw.circle(
        darkness,
        (0, 0, 0, 0),
        (player.x + 13, player.y + 20),
        110
    )

    screen.blit(darkness, (0, 0))

# =========================
# FASE
# =========================

def run_phase3(screen):

    keys = pygame.key.get_pressed()

    # =========================
    # MOVIMENTO
    # =========================

    if keys[pygame.K_w]:
        player.y -= player_speed

    if keys[pygame.K_s]:
        player.y += player_speed

    if keys[pygame.K_a]:
        player.x -= player_speed

    if keys[pygame.K_d]:
        player.x += player_speed

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
    # CARROS
    # =========================

    for car in cars:

        car.x += car_speed

        if car.x > WIDTH + 100:
            car.x = random.randint(-400, -100)

        # colisão com carro
        if player.colliderect(car):
            reset_game()

    # =========================
    # ATRAVESSAR FORA DA FAIXA
    # =========================

    if player.colliderect(road):

        if not player.colliderect(crosswalk):
            reset_game()

    # =========================
    # CHEGOU AO HOSPITAL
    # =========================

    if player.colliderect(hospital):
        return "menu"

    # =========================
    # FUNDO
    # =========================

    screen.fill(SIDEWALK)

    pygame.draw.rect(screen, SKY, (0, 0, WIDTH, 160))

    pygame.draw.rect(screen, GREEN, (0, 540, WIDTH, 60))

    # =========================
    # RUA
    # =========================

    pygame.draw.rect(screen, ROAD, road)

    # =========================
    # FAIXA
    # =========================

    for y in range(210, 340, 25):

        pygame.draw.rect(
            screen,
            WHITE,
            (365, y, 50, 14),
            border_radius=4
        )

    # =========================
    # PISO TÁTIL
    # =========================

    for tile in tactile_path:

        pygame.draw.rect(
            screen,
            YELLOW,
            tile,
            border_radius=3
        )

        for x in range(tile.x + 4, tile.x + tile.width, 8):

            for y in range(tile.y + 4, tile.y + tile.height, 8):

                pygame.draw.circle(
                    screen,
                    (180, 150, 20),
                    (x, y),
                    2
                )

    # =========================
    # CARROS
    # =========================

    for car in cars:
        draw_car(screen, car)

    # =========================
    # HOSPITAL
    # =========================

    draw_hospital(screen)

    # =========================
    # PLAYER
    # =========================

    draw_player(screen)

    # =========================
    # TEXTO
    # =========================

    text = font.render(
        "Siga o piso tatil e atravesse na faixa",
        True,
        BLACK
    )

    screen.blit(text, (140, 20))

    # =========================
    # VISÃO
    # =========================

    draw_vision_effect(screen)

    return None