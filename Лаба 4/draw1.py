import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 800))

cyellow = (255, 255 ,0)
cred = (255, 0, 0)
cblack = (0, 0, 0)
x1 = 400
y1 = 400
r = 200
r2=40
r4=20
r3=15
r5=10
x2=300
y2=350
x3=500

abrl = []
abrr = []

xbrl=[350, 360, 300, 290]
ybrl=[340, 335, 305, 310]

abrl = zip(xbrl, ybrl)
abrl = [(365, 305), (350,325),(220,250),(190,230)]

xbrr=[450, 440, 480, 490]
ybrr=[340, 335, 320, 324]

abrr = zip(xbrr, ybrr)
abrr = [(450,340),(440,315),(540,280),(555,310)]

yu=500

circle(screen, cyellow, (x1, y1), r)
circle(screen, cred, (x2, y2), r2)
circle(screen, cblack, (x2, y2), r3)
circle(screen, cred, (x3, y2), r4)
circle(screen, cblack, (x3, y2), r5)

polygon(screen, cblack, abrl)
polygon(screen, cblack, abrr)

rect(screen, cblack, (295,500,210,25))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while finished == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
