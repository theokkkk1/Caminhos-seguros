import pygame
import screens.menu as draw_menu

from screens.controls import draw_controls
from screens.phase1 import run_phase1
from screens.phase2 import run_phase2

pygame.init()

# ==========================
# TELA
# ==========================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caminhos Seguros")

clock = pygame.time.Clock()

# ==========================
# ESTADOS
# ==========================

MENU = "menu"
PHASE1 = "phase1"
PHASE2 = "phase2"
CONTROLS = "controls"

current_screen = MENU

running = True

# ==========================
# LOOP PRINCIPAL
# ==========================

while running:

    clock.tick(60)

    for event in pygame.event.get():

        # FECHAR JOGO
        if event.type == pygame.QUIT:
            running = False

        # ==========================
        # CLIQUE DO MOUSE
        # ==========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # MENU
            if current_screen == MENU:

                # JOGAR
                if draw_menu.play_button.collidepoint(mouse_pos):
                    current_screen = PHASE1

                # CONTROLES
                if draw_menu.controls_button.collidepoint(mouse_pos):
                    current_screen = CONTROLS

                # SAIR
                if draw_menu.exit_button.collidepoint(mouse_pos):
                    running = False

        # ==========================
        # TECLADO
        # ==========================

        if event.type == pygame.KEYDOWN:

            # CONTROLES
            if current_screen == CONTROLS:

                if event.key == pygame.K_ESCAPE:
                    current_screen = MENU

            # FASE 1
            elif current_screen == PHASE1:

                if event.key == pygame.K_ESCAPE:
                    current_screen = MENU

            # FASE 2
            elif current_screen == PHASE2:

                if event.key == pygame.K_ESCAPE:
                    current_screen = MENU

    # ==========================
    # RENDERIZAÇÃO
    # ==========================

    if current_screen == MENU:
        draw_menu.draw_menu(screen)

    elif current_screen == CONTROLS:
        draw_controls(screen)

    elif current_screen == PHASE1:

        next_screen = run_phase1(screen)

        if next_screen:
            current_screen = next_screen

    elif current_screen == PHASE2:

        next_screen = run_phase2(screen)

        if next_screen:
            current_screen = next_screen

    pygame.display.update()

pygame.quit()