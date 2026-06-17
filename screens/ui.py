"""
Modulo de estilo compartilhado.

Centraliza paleta de cores, fontes (em cache, para nao recriar a cada
frame) e funcoes de desenho reutilizaveis (botoes, icones, texto com
sombra, gradiente) para dar uma cara mais "jogo" e consistente para o
menu e as telas de apoio (controles).
"""

import math
import pygame

pygame.font.init()

# =========================
# PALETA
# =========================

WHITE = (255, 255, 255)
BLACK = (20, 20, 25)

SKY_TOP = (78, 158, 245)
SKY_BOTTOM = (180, 224, 255)

GRASS_TOP = (96, 196, 92)
GRASS_BOTTOM = (60, 160, 70)

PANEL = (250, 250, 252)
PANEL_SHADOW = (40, 55, 80)

NAVY = (22, 30, 54)
NAVY_LIGHT = (33, 45, 78)

ACCENT = (255, 197, 61)        # dourado - destaque / hover
ACCENT_DARK = (214, 150, 28)

GREEN = (50, 190, 110)
DARK_GREEN = (24, 130, 70)

RED = (230, 70, 70)
BLUE = (60, 120, 255)

GRAY = (170, 178, 196)
DARK_GRAY = (88, 96, 114)

TEXT_LIGHT = (255, 255, 255)
TEXT_DARK = (26, 30, 44)


# =========================
# FONTES (cache)
# =========================

_font_cache = {}


def font(size, bold=False, name="Arial"):
    key = (name, size, bold)

    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont(name, size, bold=bold)

    return _font_cache[key]


# =========================
# TEXTO COM SOMBRA
# =========================

def draw_text_shadow(screen, text, size, pos, color=TEXT_LIGHT,
                      shadow=BLACK, bold=True, center=False, offset=3):

    f = font(size, bold)

    shadow_surf = f.render(text, True, shadow)
    main_surf = f.render(text, True, color)

    x, y = pos

    if center:
        x -= main_surf.get_width() // 2
        y -= main_surf.get_height() // 2

    screen.blit(shadow_surf, (x + offset, y + offset))
    screen.blit(main_surf, (x, y))

    return main_surf.get_rect(topleft=(x, y))


# =========================
# GRADIENTE VERTICAL
# =========================

def vertical_gradient(screen, rect, top_color, bottom_color):

    x, y, w, h = rect

    if h <= 0:
        return

    for i in range(h):

        t = i / h

        r = top_color[0] + (bottom_color[0] - top_color[0]) * t
        g = top_color[1] + (bottom_color[1] - top_color[1]) * t
        b = top_color[2] + (bottom_color[2] - top_color[2]) * t

        pygame.draw.line(
            screen,
            (int(r), int(g), int(b)),
            (x, y + i),
            (x + w, y + i)
        )


# =========================
# BOTAO ESTILO "JOGO"
# =========================

def draw_button(screen, rect, label, hovered=False, icon=None, t=0,
                 sub_label=None):
    """Botao com sombra, brilho dourado pulsante no hover e icone vetorial."""

    grow = 6 if hovered else 0
    btn = rect.inflate(grow, grow)

    # sombra
    pygame.draw.rect(
        screen, PANEL_SHADOW, btn.move(0, 6), border_radius=16
    )

    # brilho pulsante
    if hovered:

        glow_alpha = 90 + int(45 * math.sin(t / 8))
        glow_alpha = max(0, min(255, glow_alpha))

        glow = pygame.Surface(
            (btn.width + 26, btn.height + 26), pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow,
            (*ACCENT, glow_alpha),
            glow.get_rect(),
            border_radius=22
        )

        screen.blit(glow, (btn.x - 13, btn.y - 13))

    base_color = ACCENT if hovered else PANEL

    pygame.draw.rect(screen, base_color, btn, border_radius=16)

    # friso superior (efeito vidro)
    sheen_h = max(4, btn.height // 2 - 4)

    sheen = pygame.Surface((btn.width - 12, sheen_h), pygame.SRCALPHA)
    pygame.draw.rect(
        sheen, (255, 255, 255, 70), sheen.get_rect(), border_radius=12
    )
    screen.blit(sheen, (btn.x + 6, btn.y + 5))

    border_color = ACCENT_DARK if hovered else DARK_GRAY
    pygame.draw.rect(screen, border_color, btn, 3, border_radius=16)

    text_x_offset = 0

    if icon:
        icon_rect = pygame.Rect(btn.x + 24, btn.centery - 14, 28, 28)
        icon(screen, icon_rect, TEXT_DARK)
        text_x_offset = 16

    label_surf = font(28, True).render(label, True, TEXT_DARK)

    lx = btn.centerx - label_surf.get_width() // 2 + text_x_offset
    ly = btn.centery - label_surf.get_height() // 2

    if sub_label:
        ly -= 10

    screen.blit(label_surf, (lx, ly))

    if sub_label:
        sub_surf = font(13, False).render(sub_label, True, DARK_GRAY)
        sx = btn.centerx - sub_surf.get_width() // 2 + text_x_offset
        screen.blit(sub_surf, (sx, ly + 26))


# =========================
# ICONES VETORIAIS
# =========================

def icon_play(screen, rect, color):
    pygame.draw.polygon(
        screen,
        color,
        [
            (rect.left, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.centery)
        ]
    )


def icon_keyboard(screen, rect, color):

    pygame.draw.rect(screen, color, rect, width=3, border_radius=4)

    col_w = max(1, (rect.width - 10) // 4)
    row_h = max(1, (rect.height - 10) // 2)

    for row in range(2):
        for col in range(4):

            kx = rect.x + 4 + col * col_w
            ky = rect.y + 4 + row * row_h

            pygame.draw.rect(
                screen, color,
                (kx, ky, max(1, col_w - 2), max(1, row_h - 2))
            )


def icon_exit(screen, rect, color):

    door_w = int(rect.width * 0.55)

    pygame.draw.rect(
        screen, color, (rect.x, rect.y, door_w, rect.height),
        width=3, border_radius=3
    )

    pygame.draw.line(
        screen, color,
        (rect.x + door_w - 2, rect.centery),
        (rect.right, rect.centery),
        3
    )

    pygame.draw.polygon(
        screen, color,
        [
            (rect.right, rect.centery - 7),
            (rect.right, rect.centery + 7),
            (rect.right + 7, rect.centery)
        ]
    )


def icon_back(screen, rect, color):

    pygame.draw.line(
        screen, color,
        (rect.right, rect.centery),
        (rect.left, rect.centery),
        4
    )

    pygame.draw.polygon(
        screen, color,
        [
            (rect.left + 11, rect.top),
            (rect.left, rect.centery),
            (rect.left + 11, rect.bottom)
        ]
    )


# =========================
# PAINEL ARREDONDADO
# =========================

def draw_panel(screen, rect, color=PANEL, border=DARK_GRAY,
                border_width=3, radius=20, shadow_offset=6):

    pygame.draw.rect(
        screen, PANEL_SHADOW,
        rect.move(0, shadow_offset), border_radius=radius
    )

    pygame.draw.rect(screen, color, rect, border_radius=radius)

    if border_width:
        pygame.draw.rect(
            screen, border, rect, border_width, border_radius=radius
        )


# =========================
# ESPERA SEM CONGELAR EVENTOS
# =========================

def pause(ms=900):
    """Mantem a fila de eventos viva durante uma pequena pausa,
    evitando que o SO acuse o jogo de 'nao esta respondendo'."""

    start = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start < ms:
        pygame.event.pump()
        pygame.time.delay(10)