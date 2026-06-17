import pygame

from screens import ui

pygame.init()

WIDTH = 800
HEIGHT = 600

# botao de voltar (clicavel, alem do ESC)
back_button = pygame.Rect(300, 500, 200, 56)

_t = 0

_controls = [
    ("W A S D  /  SETAS", "Mover o personagem"),
    ("E", "Pegar e usar itens (faixa, rampa, botao do semaforo)"),
    ("ESC", "Voltar ao menu"),
    ("MOUSE", "Navegar e clicar nos botoes do menu"),
]


def draw_controls(screen):

    global _t
    _t += 1

    mouse_pos = pygame.mouse.get_pos()

    # fundo
    ui.vertical_gradient(screen, (0, 0, WIDTH, HEIGHT), ui.SKY_TOP, (60, 70, 110))

    # selo / titulo
    ui.draw_text_shadow(
        screen, "CONTROLES", 50, (WIDTH // 2, 78),
        color=ui.WHITE, center=True
    )

    subtitle = ui.font(16, False).render(
        "Confira como jogar antes de seguir caminho", True, ui.WHITE
    )
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 118))

    # painel com a lista de comandos
    panel = pygame.Rect(110, 160, 580, 300)
    ui.draw_panel(screen, panel, color=ui.PANEL, radius=22)

    row_y = panel.y + 26

    for key, description in _controls:

        key_font = ui.font(20, True)
        key_surf = key_font.render(key, True, ui.TEXT_DARK)

        key_box = pygame.Rect(panel.x + 26, row_y, max(120, key_surf.get_width() + 24), 38)

        pygame.draw.rect(screen, ui.ACCENT, key_box, border_radius=10)
        pygame.draw.rect(screen, ui.ACCENT_DARK, key_box, 2, border_radius=10)

        screen.blit(
            key_surf,
            (key_box.centerx - key_surf.get_width() // 2,
             key_box.centery - key_surf.get_height() // 2)
        )

        desc_font = ui.font(18, False)
        desc_surf = desc_font.render(description, True, ui.TEXT_DARK)
        screen.blit(desc_surf, (panel.x + 220, row_y + 9))

        row_y += 64

    # botao voltar
    hovered = back_button.collidepoint(mouse_pos)
    ui.draw_button(
        screen, back_button, "VOLTAR", hovered=hovered, icon=ui.icon_back, t=_t
    )