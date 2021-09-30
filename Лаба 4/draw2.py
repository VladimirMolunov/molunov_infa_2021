import pygame
import numpy as np
from pygame.draw import *

pygame.init()

FPS = 30
size = 800
xsize = size
ysize = size
screen = pygame.display.set_mode((xsize, ysize))

cgreen = (0, 104, 52)
cpink = (255, 176, 129)
cblack = (0, 0, 0)
cwhite = (255, 255, 255)
transparent = (200, 100, 90, 0)

rect(screen, cpink, (0, 0, xsize, ysize))


def leaf(surf, xa, ya, xb, yb):
    ellipse(surf, cgreen, (xa, ya, xb, yb))


def grect(xa, ya, width, height, x):
    polygon(screen, cgreen, [(xa, ya), (xa+width*np.cos(x), ya+width*np.sin(x)),
                             (xa + width*np.cos(x) - height * np.sin(x), ya + width * np.sin(x) + height * np.cos(x)),
                             (xa - height*np.sin(x), ya + height * np.cos(x))])


def duga(xa, ya, xb, yb, angle1, angle2):
    arc(screen, cgreen, (xa, ya, xb-xa, yb-ya), angle1, angle2, 2)


rightmove = size / 200 * 0
rightup = size / 200 * -10
x1 = size / 200 * 100 + rightmove
y1 = size / 200 * 150 + rightup
w1 = size / 200 * 6
h1 = size / 200 * 24
gap = size / 200 * 4
initial = size / 200 * 8
leftmove = size / 200 * 20
leftup = size / 200 * -10

grect(x1, y1 + initial, w1, h1 + initial, 0)
grect(x1, y1 - gap - h1, w1, h1 + initial, 0)
grect(x1 + w1 + 3 * gap / 4, y1 + gap - 3 * h1, w1, h1 + 3 * gap, np.pi / 12)
grect(x1 + 2 * w1 + 3.4 * gap, y1 - gap - 3.4 * h1 - 5 * gap, w1 - gap / 2, h1 + 3.5 * gap, np.pi / 8)

x1 = size / 200 * 60 - leftmove
y1 = size / 200 * 165 + leftup
w1 = size / 200 * 3
h1 = size / 200 * 12
gap = size / 200 * 2
initial = size / 200 * 9
leaflength = size / 8
leafhight = size / 200 * 4

grect(x1, y1 + initial, w1, h1 + initial, 0)
grect(x1, y1 - gap - h1, w1, h1 + initial, 0)
grect(x1 + w1 + gap / 2, y1 - 4 * gap - 2 * h1, w1, h1 + 2 * gap, np.pi / 12)
grect(x1 + 2 * w1 + 3 * gap, y1 - 6 * gap - 2.7 * h1 - 5 * gap, w1 - gap / 2, h1 + 4.5 * gap, np.pi / 8)

surface = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
rect(surface, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
leaf(surface, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
leaf(surface, size / 200 * 20, size / 200 * 28, leaflength, leafhight)
leaf(surface, size / 200 * 22, size / 200 * 36, leaflength, leafhight)
leaf(surface, size / 200 * 23, size / 200 * 44, leaflength, leafhight)
leaf(surface, size / 200 * 20, size / 200 * 56, leaflength, leafhight)

surface2 = pygame.transform.rotate(surface, 75)
surface3 = pygame.transform.rotate(surface, -75)
surface3 = pygame.transform.scale(surface3, (int(size / 8 * 3), int(size / 8 * 3)))
screen.blit(surface2, (size / 800 * 24 + rightmove, size / 800 * 50 + rightup))
screen.blit(surface3, (size / 800 * 506 + rightmove, size / 800 * 164 + rightup))

threeleaves = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
rect(threeleaves, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
leaf(threeleaves, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
leaf(threeleaves, size / 200 * 18, size / 200 * 30, leaflength, leafhight)
leaf(threeleaves, size / 200 * 20, size / 200 * 40, leaflength, leafhight)

threeleaves1 = pygame.transform.rotate(threeleaves, -70)
threeleaves1 = pygame.transform.scale(threeleaves1, (int(size / 32 * 11), int(size / 32 * 11)))
threeleaves2 = pygame.transform.rotate(threeleaves, 250)
threeleaves2 = pygame.transform.scale(threeleaves2, (int(size / 32 * 13), int(size / 32 * 13)))
screen.blit(threeleaves1, (size / 200 * 104 + rightmove, size / 200 * 85 + rightup))
screen.blit(threeleaves2, (size / 200 * 19 + rightmove, size / 200 * 98 + rightup))

leaflength = size / 6

threemoreleaves = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
rect(threemoreleaves, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
leaf(threemoreleaves, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
leaf(threemoreleaves, size / 200 * 18, size / 200 * 30, leaflength, leafhight)
leaf(threemoreleaves, size / 200 * 20, size / 200 * 40, leaflength, leafhight)

fiveleaves = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
rect(fiveleaves, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
leaf(fiveleaves, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
leaf(fiveleaves, size / 200 * 20, size / 200 * 26, leaflength, leafhight)
leaf(fiveleaves, size / 200 * 22, size / 200 * 32, leaflength, leafhight)
leaf(fiveleaves, size / 200 * 23, size / 200 * 38, leaflength, leafhight)
leaf(fiveleaves, size / 200 * 20, size / 200 * 44, leaflength, leafhight)

fiveleaves1 = pygame.transform.rotate(fiveleaves, -80)
fiveleaves1 = pygame.transform.scale(fiveleaves1, (int(size / 16 * 3), int(size / 16 * 3)))
fiveleaves2 = pygame.transform.rotate(fiveleaves, 255)
fiveleaves2 = pygame.transform.scale(fiveleaves2, (int(size / 14 * 3), int(size / 14 * 3)))
screen.blit(fiveleaves1, (size / 800 * 282 - leftmove, size / 800 * 410 + leftup))
screen.blit(fiveleaves2, (size / 800 * 92 - leftmove, size / 800 * 415 + leftup))

threemoreleaves1 = pygame.transform.rotate(threemoreleaves, -80)
threemoreleaves1 = pygame.transform.scale(threemoreleaves1, (int(size / 16 * 3), int(size / 16 * 3)))
threemoreleaves2 = pygame.transform.rotate(threemoreleaves, 80)
threemoreleaves2 = pygame.transform.scale(threemoreleaves2, (int(size / 16 * 3), int(size / 16 * 3)))
screen.blit(threemoreleaves1, (size / 200 * 54 - leftmove, size / 200 * 132 + leftup))
screen.blit(threemoreleaves2, (size / 200 * 31 - leftmove, size / 200 * 139 + leftup))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while finished is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
