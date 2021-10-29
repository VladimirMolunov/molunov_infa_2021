import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))


fps = 60
spr = Sprite(200, 200, 300, 500)
screen = pygame.display.set_mode((800, 800))
group = pygame.sprite.Group()
group.add(spr)
group.draw(screen)
pygame.display.update()
finished = False
clock = pygame.time.Clock()
while not finished:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
