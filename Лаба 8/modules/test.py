import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))


fps = 60
spr = Sprite(200, 200, 300, 500)
llist = [spr]
screen = pygame.display.set_mode((800, 800))
group = pygame.sprite.Group()
group.add(llist[0])
pygame.display.update()
finished = False
clock = pygame.time.Clock()
while not finished:
    clock.tick(fps)
    screen.fill((255, 255, 255))
    group.update()
    group.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            llist.pop()
    pygame.display.update()
