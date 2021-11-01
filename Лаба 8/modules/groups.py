from pygame.sprite import Group
from pathlib import Path

transparent = (255, 255, 255, 0)

bullet_group = Group()
weapon_group = Group()
target_group = Group()

group_list = [bullet_group, weapon_group, target_group]

bg = Path('modules', 'bg.jpg').resolve()
