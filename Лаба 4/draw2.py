import pygame
import numpy as np
from pygame.draw import *
from pygame import transform

pygame.init()

FPS = 30
size = 800
screen = pygame.display.set_mode((size, size))

cgreen = (0, 104, 52)
cpink = (255, 176, 129)
cblack = (0, 0, 0)
cwhite = (255, 255, 255)
transparent = (200, 100, 90, 0)

rect(screen, cpink, (0, 0, size, size))


def leaf(surf, xa, ya, xb, yb):
    ellipse(surf, cgreen, (xa, ya, xb, yb))


def grect(xa, ya, width, height, x):
    polygon(screen, cgreen, [(xa, ya), (xa+width*np.cos(x), ya+width*np.sin(x)),
                             (xa+width*np.cos(x)-height*np.sin(x), ya+width*np.sin(x)+height*np.cos(x)),
                             (xa-height*np.sin(x), ya+height*np.cos(x))])


def duga(xa, ya, xb, yb, angle1, angle2):
    arc(screen, cgreen, (xa, ya, xb-xa, yb-ya), angle1, angle2, 2)


x1 = size / 2
y1 = size / 4 * 3
w1 = size / 100 * 3
h1 = size / 25 * 3
a1 = 0
gap = size / 50

grect(x1, y1, w1, h1, 0)
grect(x1, y1-gap-h1, w1, h1, 0)
grect(x1+w1-gap/2, y1-gap-2*h1, w1, h1-gap, np.pi/12)
grect(x1+2*w1+2*gap, y1-gap-2.7*h1-5*gap, w1-gap/2, h1+3.5*gap, np.pi/8)

x1 = size / 10 * 3
y1 = size / 40 * 33
w1 = size / 200 * 3
h1 = size / 50 * 3
a1 = 0
gap = size / 100

grect(x1, y1, w1, h1, 0)
grect(x1, y1-gap-h1, w1, h1, 0)
grect(x1+w1+gap/2, y1-4*gap-2*h1, w1, h1+2*gap, np.pi/12)
grect(x1+2*w1+3*gap, y1-6*gap-2.7*h1-5*gap, w1-gap/2, h1+4.5*gap, np.pi/8)

surface = pygame.Surface((size / 8 * 3, size / 8 * 3), pygame.SRCALPHA)
rect(surface, transparent, (0, 0, 300, 300))
leaf(surface, 80, 80, 80, 16)
leaf(surface, 96, 104, 80, 16)
leaf(surface, 104, 128, 80, 16)
leaf(surface, 88, 160, 80, 16)
leaf(surface, 92, 200, 80, 16)
surface2 = pygame.transform.rotate(surface, 55)
surface3 = pygame.transform.rotate(surface, -70)
surface3 = pygame.transform.scale(surface3, (300, 300))
surface4 = pygame.transform.rotate(surface, 55)
surface4 = pygame.transform.scale(surface4, (220, 220))

screen.blit(surface2, (24, 50))
screen.blit(surface3, (458, 164))
screen.blit(surface4, (86, 370))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while finished == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
