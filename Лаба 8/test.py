from pathlib import Path
from math import atan2
import pygame

pygame.init()
drg = []
for i in range(1, 58, 1):
    txt = 'frame (' + str(i) + ').gif'
    drg.append(pygame.image.load(Path('dragon', txt)).convert_alpha())


def sh(surface: pygame.Surface):
    mask = pygame.mask.from_surface(surface)
    w = surface.get_width()
    h = surface.get_height()
    s1 = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(w):
        for j in range(h):
            if mask.get_at((i, j)) == 1:
                s1.set_at((i, j), (255, 0, 0, 128))
    surface.blit(s1, (0, 0))
    return surface
