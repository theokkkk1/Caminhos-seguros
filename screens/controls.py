import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_controls(screen):

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 60)

    screen.fill(WHITE)

    title = big_font.render("CONTROLES", True, BLACK)
    screen.blit(title, (240, 120))

    wasd = font.render("W A S D  -> Movimento", True, BLACK)
    screen.blit(wasd, (220, 250))

    install = font.render("E -> Instalar melhorias", True, BLACK)
    screen.blit(install, (180, 320))

    back = font.render("ESC -> Voltar ao menu", True, BLACK)
    screen.blit(back, (220, 420))