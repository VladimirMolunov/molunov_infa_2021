import pygame
from pathlib import Path

bullet_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()

bg = Path('modules', 'bg.jpg').resolve()
