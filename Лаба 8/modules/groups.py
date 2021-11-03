from pygame.sprite import Group

transparent = (255, 255, 255, 0)

bullet_group = Group()
weapon_group = Group()
target_group = Group()
animated_group = Group()
healthbar_group = Group()

group_list = [bullet_group, weapon_group, target_group, animated_group, healthbar_group]
