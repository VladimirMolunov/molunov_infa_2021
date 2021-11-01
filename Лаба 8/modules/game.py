import math
import pygame
from pathlib import Path

from modules import bullets, weapons, targets
from modules.buttons import Menu
from modules.menus import menu_list
from modules.groups import group_list
from modules.classes import Showable, DrawablesList, Background

target_count = 2
score_for_catch = 1


class Game(Showable):
    def __init__(self, target_color, gun_color, gun_charged_color, gun_fully_charged_color, colors):
        """
        Создаёт окно с игрой
        :param target_color: цвет мишени
        :param gun_color: цвет орудия
        :param gun_charged_color: цвет заряженного орудия
        :param gun_fully_charged_color: цвет полностью заряженного орудия
        :param colors: список возможных цветов снарядов
        """
        Showable.__init__(self)
        self.target_color = target_color
        self.ball_colors = colors
        self.gun_color = gun_color
        self.gun_charged_color = gun_charged_color
        self.gun_fully_charged_color = gun_fully_charged_color
        self.clock = pygame.time.Clock()

    def gun_game(self):
        score = 0
        bullet_list = DrawablesList()
        target_list = DrawablesList()
        gun = weapons.SimpleCannon(self.gun_color, self.gun_charged_color, self.gun_fully_charged_color)
        for i in range(target_count):
            target_list.append(targets.BallTarget(self.target_color))
        bg = Background(Path('modules', 'bg.jpg').resolve())
        finished = False

        while not finished:
            bg.blit()
            for group in group_list:
                group.draw(self.screen)
            pygame.display.update()

            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    gun.charge()
                elif event.type == pygame.MOUSEBUTTONUP:
                    bullet_list.append(gun.fire_ball(event, self.ball_colors))
                elif event.type == pygame.MOUSEMOTION:
                    gun.targetting(event)

            gun.config_sprite()
            for target in target_list:
                target.move()
            for ball in bullet_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target.sprite.kill()
                            target.__init__(self.target_color)
                            score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    bullet_list.smart_pop(0)
            gun.power_up()
        pygame.quit()
        return score

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.draw.rect(screen, (255, 255, 0), (100, 100, 200, 100))
        menu_number = 0  # номер текущего меню
        finished = False
        while not finished:
            current_menu = menu_list[menu_number]
            current_menu.blit()
            pygame.display.update()
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                else:
                    if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                        i = current_menu.goto(event)
                        if i >= 0:
                            menu_number = i
                            current_menu = menu_list[menu_number]
        pygame.quit()
