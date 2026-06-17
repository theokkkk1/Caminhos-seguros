import math

import pygame

from screens import ui

pygame.init()

WIDTH = 800
HEIGHT = 600

# =========================
# BOTOES (posicao/clique)
# =========================

play_button = pygame.Rect(275, 252, 250, 64)
controls_button = pygame.Rect(275, 332, 250, 64)
exit_button = pygame.Rect(275, 412, 250, 64)

# contador de frames usado para as animacoes (nuvens, sol, personagem)
_t = 0


# =========================
# CENARIO
# =========================

def _draw_cloud(screen, x, y, scale=1.0):

    pygame.draw.circle(screen, ui.WHITE, (int(x), int(y)), int(28 * scale))
    pygame.draw.circle(screen, ui.WHITE, (int(x + 32 * scale), int(y - 6 * scale)), int(34 * scale))
    pygame.draw.circle(screen, ui.WHITE, (int(x + 64 * scale), int(y)), int(26 * scale))


def _draw_background(screen, t):

    # ceu em degrade
    ui.vertical_gradient(screen, (0, 0, WIDTH, 250), ui.SKY_TOP, ui.SKY_BOTTOM)

    # grama
    ui.vertical_gradient(screen, (0, 480, WIDTH, 120), ui.GRASS_TOP, ui.GRASS_BOTTOM)

    # calcada
    pygame.draw.rect(screen, (214, 214, 214), (0, 250, WIDTH, 230))

    # rua central
    pygame.draw.rect(screen, (45, 45, 45), (320, 0, 160, HEIGHT))

    scroll = int(t * 1.2) % 90

    for y in range(-90 + scroll, HEIGHT, 90):
        pygame.draw.rect(screen, ui.WHITE, (392, y, 16, 50), border_radius=5)

    # sol com leve pulso
    sun_r = 42 + int(4 * math.sin(t / 30))
    pygame.draw.circle(screen, ui.ACCENT_DARK, (680, 72), sun_r + 6)
    pygame.draw.circle(screen, ui.ACCENT, (680, 72), sun_r)

    # nuvens deslizando
    drift = math.sin(t / 90) * 14
    _draw_cloud(screen, 120 + drift, 85, 1.0)
    _draw_cloud(screen, 470 - drift, 118, 0.75)

    # hospital
    hospital = pygame.Rect(600, 320, 110, 110)

    pygame.draw.rect(screen, (236, 236, 240), hospital, border_radius=16)
    pygame.draw.rect(screen, ui.RED, (645, 340, 20, 60))
    pygame.draw.rect(screen, ui.RED, (625, 360, 60, 20))
    pygame.draw.rect(screen, (180, 220, 255), (612, 332, 16, 16), border_radius=4)
    pygame.draw.rect(screen, (180, 220, 255), (682, 332, 16, 16), border_radius=4)
    pygame.draw.rect(screen, ui.DARK_GRAY, (650, 405, 12, 20), border_radius=4)

    # arvores com leve balanco
    trees = [(90, 440), (180, 520), (560, 520)]

    for tx, ty in trees:

        sway = math.sin(t / 45 + tx) * 2

        pygame.draw.rect(screen, (120, 70, 20), (tx + 12, ty + 20, 14, 40))
        pygame.draw.circle(screen, ui.DARK_GREEN, (int(tx + 18 + sway), ty + 10), 30)
        pygame.draw.circle(screen, ui.GREEN, (int(tx + 30 + sway), ty + 5), 24)

    # personagem com balanco (idle)
    px = 120
    py = 390 + math.sin(t / 14) * 3

    pygame.draw.circle(screen, (255, 220, 180), (px + 13, int(py + 10)), 12)
    pygame.draw.rect(screen, ui.BLUE, (px + 4, int(py + 20), 18, 20), border_radius=4)

    pygame.draw.line(screen, ui.BLACK, (px + 8, int(py + 40)), (px + 5, int(py + 50)), 3)
    pygame.draw.line(screen, ui.BLACK, (px + 18, int(py + 40)), (px + 22, int(py + 50)), 3)
    pygame.draw.line(screen, ui.BLACK, (px + 4, int(py + 26)), (px - 4, int(py + 34)), 3)
    pygame.draw.line(screen, ui.BLACK, (px + 22, int(py + 26)), (px + 30, int(py + 34)), 3)

    # escurece levemente o cenario para os botoes terem contraste
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 14, 26, 70))
    screen.blit(overlay, (0, 0))


# =========================
# MENU
# =========================

def draw_menu(screen):

    global _t
    _t += 1

    mouse_pos = pygame.mouse.get_pos()

    _draw_background(screen, _t)

    # =========================
    # SELO
    # =========================

    badge_font = ui.font(15, True)
    badge = badge_font.render("JOGO EDUCATIVO  -  MOBILIDADE URBANA", True, ui.NAVY)

    badge_rect = pygame.Rect(0, 0, badge.get_width() + 28, 30)
    badge_rect.centerx = WIDTH // 2
    badge_rect.y = 18

    pygame.draw.rect(screen, ui.ACCENT, badge_rect, border_radius=15)
    pygame.draw.rect(screen, ui.ACCENT_DARK, badge_rect, 2, border_radius=15)
    screen.blit(badge, (badge_rect.centerx - badge.get_width() // 2, badge_rect.y + 6))

    # =========================
    # TITULO (com leve "respiro")
    # =========================

    pulse = 1.0 + 0.015 * math.sin(_t / 20)

    title_size = int(52 * pulse)

    title_font = ui.font(title_size, True)

    title_shadow = title_font.render("CAMINHOS SEGUROS", True, (0, 0, 0))
    title = title_font.render("CAMINHOS SEGUROS", True, ui.WHITE)
    title_accent = title_font.render("CAMINHOS SEGUROS", True, ui.ACCENT)

    tx = WIDTH // 2 - title.get_width() // 2

    screen.blit(title_shadow, (tx + 5, 64))
    screen.blit(title_accent, (tx + 1, 60))
    screen.blit(title, (tx, 60))

    subtitle_font = ui.font(18, False)
    subtitle = subtitle_font.render(
        "Atravesse com seguranca e ajude a tornar a cidade acessivel para todos",
        True, ui.WHITE
    )
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 122))

    # =========================
    # PAINEL DOS BOTOES
    # =========================

    panel = pygame.Rect(235, 220, 330, 280)
    ui.draw_panel(screen, panel, color=(255, 255, 255), radius=22)

    buttons = [
        (play_button, "JOGAR", ui.icon_play, None),
        (controls_button, "CONTROLES", ui.icon_keyboard, None),
        (exit_button, "SAIR", ui.icon_exit, None),
    ]

    for button, text, icon, sub in buttons:

        hovered = button.collidepoint(mouse_pos)
        ui.draw_button(screen, button, text, hovered=hovered, icon=icon, t=_t, sub_label=sub)

    # =========================
    # RODAPE - CONTROLES RAPIDOS
    # =========================

    hint_font = ui.font(15, False)

    hints = "WASD / SETAS  movimento      E  usar item      ESC  voltar"
    hint_surf = hint_font.render(hints, True, ui.WHITE)

    hint_bg = pygame.Rect(0, 0, hint_surf.get_width() + 24, 30)
    hint_bg.centerx = WIDTH // 2
    hint_bg.y = HEIGHT - 40

    bg_surf = pygame.Surface(hint_bg.size, pygame.SRCALPHA)
    pygame.draw.rect(bg_surf, (0, 0, 0, 110), bg_surf.get_rect(), border_radius=14)
    screen.blit(bg_surf, hint_bg.topleft)

    screen.blit(hint_surf, (hint_bg.x + 12, hint_bg.y + 6))