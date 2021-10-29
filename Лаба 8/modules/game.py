import math
import pygame
from modules import classes, bullets, weapons, targets
from modules.classes import *
from random import randint, choice

target_count = 2
score_for_catch = 1


class Game(Drawable):
    def __init__(self, target_color, background_color, gun_color, gun_charged_color, colors):
        Drawable.__init__(self)
        self.target_color = target_color
        self.background_color = background_color
        self.ball_colors = colors
        self.gun_color = gun_color
        self.gun_charged_color = gun_charged_color

    def main(self):
        score = 0
        target_list = []
        ball_list = []
        clock = pygame.time.Clock()
        gun = weapons.Gun(self.gun_color, self.gun_charged_color)
        for i in range(target_count):
            target_list.append(targets.BallTarget(self.target_color))
        finished = False

        while not finished:
            self.screen.fill(self.background_color)
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
                    ball_list.append(gun.fire_ball(event, self.ball_colors))
                elif event.type == pygame.MOUSEMOTION:
                    gun.targetting(event)

            for target in target_list:
                target.move()
            for ball in ball_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target.__init__(self.target_color)
                            score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    ball_list.pop(0)
            gun.power_up()
        pygame.quit()
        return score
