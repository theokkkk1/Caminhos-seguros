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

player = pygame.Rect(120, 500, 26, 42)
player_speed = 5

# =========================
# ITENS
# =========================

crosswalk_item = pygame.Rect(200, 430, 40, 40)
ramp_item = pygame.Rect(640, 500, 40, 40)

has_crosswalk = False
has_ramp = False

# =========================
# BARREIRA
# =========================

barrier = pygame.Rect(520, 300, 200, 100)

left_block = pygame.Rect(
    barrier.x - 25,
    barrier.y,
    25,
    barrier.height
)

right_block = pygame.Rect(
    barrier.x + barrier.width - 5,
    barrier.y - 40,
    70,
    barrier.height + 80
)

# =========================
# CARROS
# =========================

cars = []

for i in range(3):

    cars.append(
        pygame.Rect(
            365,
            random.randint(-600, -50),
            45,
            80
        )
    )

car_speed = 5

# =========================
# ÁRVORES
# =========================

trees = [
    pygame.Rect(80, 180, 70, 70),
    pygame.Rect(80, 390, 70, 70),
    pygame.Rect(560, 430, 70, 70),
]

# =========================
# RESET
# =========================

def reset_game():

    global has_crosswalk
    global has_ramp

    player.x = 120
    player.y = 500

    has_crosswalk = False
    has_ramp = False

    for car in cars:
        car.y = random.randint(-600, -50)

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
# GAME
# =========================

def run_phase1(screen):

    global has_crosswalk
    global has_ramp

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

    near_crosswalk = player.colliderect(crosswalk_item)
    near_ramp = player.colliderect(ramp_item)

    if near_crosswalk and keys[pygame.K_e]:
        has_crosswalk = True

    if near_ramp and keys[pygame.K_e]:
        has_ramp = True

    # =========================
    # GAME OVER SEM FAIXA
    # =========================

    road_zone = pygame.Rect(320, 0, 160, HEIGHT)

    if player.colliderect(road_zone):

        if not has_crosswalk:

            game_over_font = pygame.font.SysFont("Arial", 45, bold=True)

            txt = game_over_font.render(
                "Use a faixa",
                True,
                RED
            )

            screen.blit(txt, (250, 260))

            pygame.display.update()
            pygame.time.delay(1200)

            reset_game()

    # =========================
    # COLISÃO BARREIRA
    # =========================

    if not has_ramp:

        if player.colliderect(barrier):
            player.x = old_x
            player.y = old_y

        if player.colliderect(left_block):
            player.x = old_x
            player.y = old_y

        if player.colliderect(right_block):
            player.x = old_x
            player.y = old_y

    # =========================
    # CARROS
    # =========================

    for car in cars:

        if not has_crosswalk:
            car.y += car_speed

        if car.y > HEIGHT:
            car.y = random.randint(-400, -100)

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

    for x in range(0, WIDTH, 30):
        pygame.draw.line(screen, (190, 190, 190), (x, 90), (x, HEIGHT))

    for y in range(90, HEIGHT, 30):
        pygame.draw.line(screen, (190, 190, 190), (0, y), (WIDTH, y))

    pygame.draw.rect(screen, ROAD, (320, 0, 160, HEIGHT))

    for y in range(0, HEIGHT, 90):

        pygame.draw.rect(
            screen,
            WHITE,
            (392, y, 16, 50),
            border_radius=5
        )

    # faixa colocada
    if has_crosswalk:

        for i in range(6):

            pygame.draw.rect(
                screen,
                WHITE,
                (
                    325 + i * 27,
                    420,
                    18,
                    55
                ),
                border_radius=3
            )

    for tree in trees:
        draw_tree(screen, tree)

    # barreira
    pygame.draw.rect(
        screen,
        GRAY,
        barrier,
        border_radius=12
    )

    for y in range(barrier.y + 12, barrier.y + 90, 18):

        pygame.draw.line(
            screen,
            DARK_GRAY,
            (barrier.x, y),
            (barrier.x + barrier.width, y),
            3
        )

    # hospital
    pygame.draw.rect(
        screen,
        (240, 240, 240),
        (620, 110, 95, 95),
        border_radius=16
    )

    pygame.draw.rect(screen, (180, 220, 255), (635, 120, 16, 16), border_radius=4)
    pygame.draw.rect(screen, (180, 220, 255), (680, 120, 16, 16), border_radius=4)

    pygame.draw.rect(screen, RED, (658, 130, 20, 55))
    pygame.draw.rect(screen, RED, (640, 148, 55, 20))

    pygame.draw.rect(screen, (70, 70, 70), (672, 180, 12, 20), border_radius=4)

    # placa rua
    




    # =========================
    # ITENS
    # =========================

    if not has_crosswalk:

        pygame.draw.rect(
            screen,
            WHITE,
            crosswalk_item,
            border_radius=4
        )

        for y in range(435, 465, 6):

            pygame.draw.line(
                screen,
                BLACK,
                (205, y),
                (235, y),
                3
            )

        item_font = pygame.font.SysFont("Arial", 20, bold=True)

        txt = item_font.render("Faixa", True, BLACK)

        screen.blit(txt, (175, 475))

    if not has_ramp:

        pygame.draw.rect(
            screen,
            BLUE,
            ramp_item,
            border_radius=8
        )

        pygame.draw.circle(screen, WHITE, (660, 514), 7, 2)

        pygame.draw.line(screen, WHITE, (660, 521), (660, 530), 2)
        pygame.draw.line(screen, WHITE, (660, 524), (652, 534), 2)
        pygame.draw.line(screen, WHITE, (660, 524), (668, 534), 2)

        item_font = pygame.font.SysFont("Arial", 20, bold=True)

        txt = item_font.render("Rampa", True, BLACK)

        screen.blit(txt, (635, 548))

    # =========================
    # APERTE E
    # =========================

    hint_font = pygame.font.SysFont("Arial", 22, bold=True)

    if near_crosswalk and not has_crosswalk:

        txt = hint_font.render(
            "APERTE E",
            True,
            BLACK
        )

        screen.blit(txt, (150, 390))

    if near_ramp and not has_ramp:

        txt = hint_font.render(
            "APERTE E",
            True,
            BLACK
        )

        screen.blit(txt, (610, 465))

    # =========================
    # CARROS
    # =========================

    for car in cars:
        draw_car(screen, car)

    # =========================
    # PLAYER
    # =========================

    draw_player(screen)

    # =========================
    # HUD
    # =========================

    hud = pygame.Rect(10, 10, 300, 105)

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        hud,
        border_radius=12
    )

    hud_font = pygame.font.SysFont("Arial", 26, bold=True)

    faixa_text = hud_font.render(
        f"Faixa: {'SIM' if has_crosswalk else 'NAO'}",
        True,
        BLACK
    )

    rampa_text = hud_font.render(
        f"Rampa: {'SIM' if has_ramp else 'NAO'}",
        True,
        BLACK
    )

    screen.blit(faixa_text, (25, 28))
    screen.blit(rampa_text, (25, 68))

        # =========================
    # VITÓRIA
    # =========================

    hospital_area = pygame.Rect(590, 60, 170, 180)

    if player.colliderect(hospital_area):

        if has_crosswalk and has_ramp:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(210)
            overlay.fill((0, 0, 0))

            screen.blit(overlay, (0, 0))

            # caixa branca
            pygame.draw.rect(
                screen,
                WHITE,
                (90, 170, 620, 220),
                border_radius=20
            )

            # fontes
            victory_font = pygame.font.SysFont(
                "Arial",
                34,
                bold=True
            )

            small_font = pygame.font.SysFont(
                "Arial",
                26
            )

            # textos
            title = victory_font.render(
                "VOCÊ CHEGOU AO HOSPITAL!",
                True,
                GREEN
            )

            desc = small_font.render(
                "Acessibilidade salva vidas.",
                True,
                BLACK
            )

            # título centralizado
            screen.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    245
                )
            )

            # descrição centralizada
            screen.blit(
                desc,
                (
                    WIDTH // 2 - desc.get_width() // 2,
                    315
                )
            )

            pygame.display.update()
            pygame.time.delay(1500)

            return "phase2"