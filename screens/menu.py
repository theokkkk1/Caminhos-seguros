
import pygame

pygame.init()

# =========================
# CORES
# =========================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SKY = (120, 190, 255)

GREEN = (40, 180, 40)
DARK_GREEN = (20, 130, 20)

GRAY = (230, 230, 230)
DARK_GRAY = (70, 70, 70)

BLUE = (60, 120, 255)

RED = (220, 50, 50)

YELLOW = (255, 225, 70)

# =========================
# FONTES
# =========================

title_font = pygame.font.SysFont("Arial", 52, bold=True)

button_font = pygame.font.SysFont("Arial", 30, bold=True)

small_font = pygame.font.SysFont("Arial", 20)

# =========================
# BOTÕES
# =========================

play_button = pygame.Rect(275, 240, 250, 65)

controls_button = pygame.Rect(275, 330, 250, 65)

exit_button = pygame.Rect(275, 420, 250, 65)

# =========================
# MENU
# =========================

def draw_menu(screen):

    mouse_pos = pygame.mouse.get_pos()

    # =========================
    # FUNDO
    # =========================

    screen.fill((210, 210, 210))

    # céu
    pygame.draw.rect(screen, SKY, (0, 0, 800, 230))

    # grama
    pygame.draw.rect(screen, GREEN, (0, 500, 800, 100))

    # rua
    pygame.draw.rect(screen, (45, 45, 45), (320, 0, 160, 600))

    # linhas da rua
    for y in range(0, 600, 90):

        pygame.draw.rect(
            screen,
            WHITE,
            (392, y, 16, 50),
            border_radius=5
        )

    # =========================
    # SOL
    # =========================

    pygame.draw.circle(screen, YELLOW, (680, 70), 45)

    # =========================
    # NUVENS
    # =========================

    pygame.draw.circle(screen, WHITE, (130, 90), 30)
    pygame.draw.circle(screen, WHITE, (160, 90), 35)
    pygame.draw.circle(screen, WHITE, (195, 90), 30)

    pygame.draw.circle(screen, WHITE, (530, 120), 25)
    pygame.draw.circle(screen, WHITE, (560, 120), 30)
    pygame.draw.circle(screen, WHITE, (590, 120), 25)

    # =========================
    # HOSPITAL
    # =========================

    hospital = pygame.Rect(600, 320, 110, 110)

    pygame.draw.rect(
        screen,
        (235, 235, 235),
        hospital,
        border_radius=16
    )

    pygame.draw.rect(screen, RED, (645, 340, 20, 60))
    pygame.draw.rect(screen, RED, (625, 360, 60, 20))

    pygame.draw.rect(
        screen,
        (180, 220, 255),
        (612, 332, 16, 16),
        border_radius=4
    )

    pygame.draw.rect(
        screen,
        (180, 220, 255),
        (682, 332, 16, 16),
        border_radius=4
    )

    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (650, 405, 12, 20),
        border_radius=4
    )

    # =========================
    # ÁRVORES
    # =========================

    trees = [
        (90, 440),
        (180, 520),
        (560, 520)
    ]

    for tx, ty in trees:

        pygame.draw.rect(
            screen,
            (120, 70, 20),
            (tx + 12, ty + 20, 14, 40)
        )

        pygame.draw.circle(
            screen,
            DARK_GREEN,
            (tx + 18, ty + 10),
            30
        )

        pygame.draw.circle(
            screen,
            GREEN,
            (tx + 30, ty + 5),
            24
        )

    # =========================
    # BONECO
    # =========================

    px = 120
    py = 390

    pygame.draw.circle(
        screen,
        (255, 220, 180),
        (px + 13, py + 10),
        12
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (px + 4, py + 20, 18, 20),
        border_radius=4
    )

    pygame.draw.line(
        screen,
        BLACK,
        (px + 8, py + 40),
        (px + 5, py + 50),
        3
    )

    pygame.draw.line(
        screen,
        BLACK,
        (px + 18, py + 40),
        (px + 22, py + 50),
        3
    )

    pygame.draw.line(
        screen,
        BLACK,
        (px + 4, py + 26),
        (px - 4, py + 34),
        3
    )

    pygame.draw.line(
        screen,
        BLACK,
        (px + 22, py + 26),
        (px + 30, py + 34),
        3
    )

    # =========================
    # TÍTULO
    # =========================

    shadow = title_font.render(
        "CAMINHOS SEGUROS",
        True,
        BLACK
    )

    title = title_font.render(
        "CAMINHOS SEGUROS",
        True,
        WHITE
    )

    screen.blit(shadow, (146, 56))
    screen.blit(title, (140, 50))

    # =========================
    # BOTÕES
    # =========================

    buttons = [
        (play_button, "JOGAR"),
        (controls_button, "CONTROLES"),
        (exit_button, "SAIR")
    ]

    for button, text in buttons:

        color = GRAY

        if button.collidepoint(mouse_pos):
            color = WHITE

        # sombra
        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (
                button.x + 4,
                button.y + 4,
                button.width,
                button.height
            ),
            border_radius=14
        )

        # botão
        pygame.draw.rect(
            screen,
            color,
            button,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            DARK_GRAY,
            button,
            3,
            border_radius=14
        )

        txt = button_font.render(
            text,
            True,
            BLACK
        )

        screen.blit(
            txt,
            (
                button.centerx - txt.get_width() // 2,
                button.centery - txt.get_height() // 2
            )
        )

    # =========================
    # CONTROLES
    # =========================

    controls = [
        "WASD -> mover",
        "E -> usar itens",
        "ESC -> voltar"
    ]

    controls_y = 520

    for control in controls:

        txt = small_font.render(
            control,
            True,
            BLACK
        )

        screen.blit(txt, (20, controls_y))

        controls_y += 24

