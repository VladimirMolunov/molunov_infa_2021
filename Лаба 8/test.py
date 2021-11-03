from pathlib import Path
from math import atan2
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
healthbar_image = pygame.image.load(Path('images', 'healthbar.png').resolve())
healthbar_inside = pygame.image.load(Path('images', 'healthbar_inside.png').resolve())

health = 1
max_health = 1

def draw_healthbar():
    """
    Рисует шкалу здоровья на поверхности и возвращает эту поверхность
    :return: объект типа pygame.Surface
    """
    surface = healthbar_image.convert_alpha()
    surface.set_colorkey((255, 255, 255))
    surface2 = healthbar_inside.convert_alpha()
    surface2.set_colorkey((255, 255, 255))
    surface = pygame.transform.scale(surface, (270, 18)).convert_alpha()
    surface2 = pygame.transform.scale(surface2, (270, 18)).convert_alpha()
    surface3 = pygame.Surface((270, 18), pygame.SRCALPHA).convert_alpha()
    surface4 = surface2.subsurface(0, 0, 267 * health / max_health, 18).convert_alpha()
    surface3.set_colorkey((255, 255, 255))
    surface3.blit(surface4, (0, 0))
    surface4.set_colorkey((255, 255, 255))
    surface.blit(surface4, (0, 0))
    return surface


finished = False
clock = pygame.time.Clock()
while not finished:
    clock.tick(60)
    screen.blit(draw_healthbar(), (200, 200))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
