import pygame
import random

from screens import ui

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
DARK_RED = (150, 20, 20)

YELLOW = (255, 225, 70)
ORANGE = (255, 150, 40)
GRAY = (120, 120, 120)

SKY = (120, 190, 255)

# =========================
# PLAYER
# =========================

player = pygame.Rect(80, 500, 26, 42)
player_speed = 4

# =========================
# ESCOLA
# =========================

school = pygame.Rect(640, 60, 120, 120)

# =========================
# PISO TATIL
# =========================
# O piso tatil agora atravessa a rua exatamente por dentro da faixa
# de pedestre pintada (antes ele contornava a faixa por fora, levando
# o jogador ao redor da rua em vez de atraves da travessia segura).

tactile_path = [
    pygame.Rect(100, 520, 40, 20),
    pygame.Rect(140, 520, 40, 20),
    pygame.Rect(180, 520, 40, 20),
    pygame.Rect(220, 520, 40, 20),
    pygame.Rect(260, 520, 40, 20),
    pygame.Rect(300, 520, 40, 20),
    pygame.Rect(340, 520, 40, 20),

    pygame.Rect(375, 480, 20, 40),
    pygame.Rect(375, 440, 20, 40),
    pygame.Rect(375, 400, 20, 40),
    pygame.Rect(375, 360, 20, 40),
    pygame.Rect(375, 320, 20, 40),
    pygame.Rect(375, 280, 20, 40),
    pygame.Rect(375, 240, 20, 40),
    pygame.Rect(375, 200, 20, 40),

    pygame.Rect(400, 180, 40, 20),
    pygame.Rect(440, 180, 40, 20),
    pygame.Rect(480, 180, 40, 20),
    pygame.Rect(520, 180, 40, 20),
    pygame.Rect(560, 180, 40, 20),
]

# =========================
# RUA
# =========================
# A rua (e a colisao de "precisa estar na faixa") cobre a LARGURA
# TOTAL da tela, porque os carros tambem trafegam de ponta a ponta.
# Antes a rua era so um trecho central (250-550) e os carros, ao
# saírem dele, ficavam visualmente "andando" por cima da calcada e
# da grama -- alem disso, dava pra desviar da faixa de pedestre
# simplesmente contornando esse trecho por fora, sem nunca precisar
# usar a faixa. Cobrindo a tela inteira corrige os dois problemas.

road = pygame.Rect(0, 200, WIDTH, 160)

# =========================
# FAIXA DE PEDESTRE
# =========================

crosswalk = pygame.Rect(330, 200, 120, 160)

# =========================
# BOTÃO DO SEMÁFORO
# =========================

crossing_button = pygame.Rect(300, 370, 42, 42)
crosswalk_active = False
button_message_timer = 0

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
stopped_car_speed = 0

# =========================
# FONTE
# =========================

font = pygame.font.SysFont("Arial", 24, bold=True)

# =========================
# RESET
# =========================

def reset_game():

    global crosswalk_active, button_message_timer

    player.x = 80
    player.y = 500

    crosswalk_active = False
    button_message_timer = 0

    for car in cars:
        car.x = random.randint(-500, -50)


def enter_phase():
    """Chamado sempre que se entra nesta fase a partir de outra tela,
    garantindo que ela comece sempre do zero."""

    reset_game()

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
# ESCOLA
# =========================

def draw_school(screen):

    pygame.draw.rect(
        screen,
        (235, 235, 235),
        school,
        border_radius=15
    )

    pygame.draw.rect(screen, (120, 80, 40), (680, 125, 40, 55))
    pygame.draw.rect(screen, SKY, (655, 85, 28, 28))
    pygame.draw.rect(screen, SKY, (717, 85, 28, 28))

    roof_points = [
        (630, 70),
        (700, 25),
        (770, 70)
    ]
    pygame.draw.polygon(screen, DARK_RED, roof_points)

    title_font = pygame.font.SysFont("Arial", 20, bold=True)
    title = title_font.render("ESCOLA", True, BLACK)
    screen.blit(title, (665, 145))


def draw_crossing_button(screen):

    button_color = GREEN if crosswalk_active else ORANGE

    pygame.draw.rect(
        screen,
        GRAY,
        crossing_button,
        border_radius=8
    )

    pygame.draw.circle(
        screen,
        button_color,
        crossing_button.center,
        14
    )

    label_font = pygame.font.SysFont("Arial", 16, bold=True)
    label = label_font.render("BOTAO", True, BLACK)
    screen.blit(label, (crossing_button.x - 8, crossing_button.y + 48))

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

    global crosswalk_active, button_message_timer

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
    # ACIONAR BOTÃO DA FAIXA
    # =========================

    if player.colliderect(crossing_button) and keys[pygame.K_e]:
        crosswalk_active = True
        button_message_timer = 120

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

        if crosswalk_active:
            car.x += stopped_car_speed
        else:
            car.x += car_speed

        if car.x > WIDTH + 100:
            car.x = random.randint(-400, -100)

        # colisão com carro
        if player.colliderect(car):
            reset_game()

    # =========================
    # ATRAVESSAR A RUA
    # =========================

    if player.colliderect(road):

        # Não pode atravessar fora da faixa
        if not player.colliderect(crosswalk):
            reset_game()

        # Mesmo na faixa, precisa apertar o botão antes
        elif not crosswalk_active:
            reset_game()

    # =========================
    # CHEGOU À ESCOLA
    # =========================

    reached_school = player.colliderect(school)

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

    if crosswalk_active:
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
    # BOTÃO DO SEMÁFORO
    # =========================

    draw_crossing_button(screen)

    # =========================
    # CARROS
    # =========================

    for car in cars:
        draw_car(screen, car)

    # =========================
    # ESCOLA
    # =========================

    draw_school(screen)

    # =========================
    # PLAYER
    # =========================

    draw_player(screen)

    # =========================
    # TEXTO
    # =========================

    text = font.render(
        "Siga o piso tatil, aperte E no botao e atravesse para chegar na escola",
        True,
        BLACK
    )

    screen.blit(text, (35, 20))

    if player.colliderect(crossing_button) and not crosswalk_active:
        help_text = font.render(
            "Aperte E para ativar a faixa de pedestre",
            True,
            BLACK
        )
        screen.blit(help_text, (160, 55))

    if button_message_timer > 0:
        active_text = font.render(
            "Faixa ativada! Atravesse com seguranca.",
            True,
            BLACK
        )
        screen.blit(active_text, (190, 55))
        button_message_timer -= 1

    # =========================
    # VISÃO
    # =========================

    draw_vision_effect(screen)

    if reached_school:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        victory_font = pygame.font.SysFont("Arial", 36, bold=True)
        small_font = pygame.font.SysFont("Arial", 24)

        title_text = victory_font.render(
            "VOCE CHEGOU A ESCOLA!", True, GREEN
        )

        info_text = small_font.render(
            "Parabens, voce completou Caminhos Seguros!", True, WHITE
        )

        screen.blit(
            title_text,
            (WIDTH // 2 - title_text.get_width() // 2, 250)
        )

        screen.blit(
            info_text,
            (WIDTH // 2 - info_text.get_width() // 2, 310)
        )

        pygame.display.update()
        ui.pause(1800)

        return "menu"

    return None