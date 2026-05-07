import pygame
import sys

from screens.menu import draw_menu
from screens.controls import draw_controls
from screens.game import run_game

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caminhos Seguros")

clock = pygame.time.Clock()

current_screen = "menu"

while True:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MENU
        if current_screen == "menu":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    current_screen = "game"

                if event.key == pygame.K_2:
                    current_screen = "controls"

        # CONTROLES
        elif current_screen == "controls":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    current_screen = "menu"

    # DESENHAR TELAS
    if current_screen == "menu":
        draw_menu(screen)

    elif current_screen == "controls":
        draw_controls(screen)

    elif current_screen == "game":
        run_game(screen)

    pygame.display.update()