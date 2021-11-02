from pathlib import Path
from math import atan2
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
img = pygame.Surface((200, 200))
pygame.draw.rect(img, (255, 0, 0), (1, 0, 200, 200))
img = pygame.transform.rotate(img, 25)

finished = False
clock = pygame.time.Clock()
while not finished:
    clock.tick(60)
    screen.blit(img, (200, 200))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()