from pathlib import Path
from math import atan2
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
drg = []
for i in range(1, 58, 1):
    txt = 'frame (' + str(i) + ').gif'
    drg.append(pygame.image.load(Path('dragon', txt)))


finished = False
clock = pygame.time.Clock()
t = 0
while not finished:
    clock.tick(60)
    t += 0.25
    t = t % 57
    print(int(t))
    screen.fill((255, 0, 0))
    screen.blit(drg[int(t)], (200, 200))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
