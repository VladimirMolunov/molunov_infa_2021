import math
from random import choice, randint
from modules import ballmod
from modules.ballmod import *
import pygame

power = 450
lifetime = 10
g = 200
alpha = 1
beta = 1

transparent = (200, 200, 200, 0)
red = (255, 0, 0)
target_red = (228, 0, 0)
gun_red = (204, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
magenta = (255, 3, 184)
cyan = (0, 255, 204)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (125, 125, 125)
ball_colors = [red, blue, yellow, green, magenta, cyan]


class Game(Drawable):
    def __init__(self):
        Drawable.__init__(self)

    def main(self):
        target_list = []
        ball_list = []
        clock = pygame.time.Clock()
        gun = Gun(grey, gun_red)
        target_list.append(Target(target_red))
        finished = False

        while not finished:
            self.screen.fill(white)
            gun.draw()
            for target_obj in target_list:
                target_obj.draw()
            for ball in ball_list:
                ball.draw()
            pygame.display.update()

            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    gun.charge()
                elif event.type == pygame.MOUSEBUTTONUP:
                    ball_list.append(gun.fire(event, ball_colors))
                elif event.type == pygame.MOUSEMOTION:
                    gun.targetting(event)

            for ball in ball_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target.__init__(target_red)
                ball.remove_life()
                if ball.live <= 0:
                    ball_list.pop(0)
            gun.power_up()
        pygame.quit()


def main():
    game = Game()
    pygame.init()
    game.main()


if __name__ == "__main__":
    main()
