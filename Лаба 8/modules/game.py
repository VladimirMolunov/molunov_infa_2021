import math
import pygame
from pathlib import Path

from modules import bullets, weapons, targets
from modules.buttons import Menu
from modules.menus import menu_list
from modules.groups import group_list
from modules.classes import Showable, GameObjectsList, Background

target_count = 2
score_for_catch = 1

red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
magenta = (255, 3, 184)
cyan = (0, 255, 204)
ball_target_red = (228, 0, 0)
cannon_grey = (102, 102, 102)
cannon_red = (255, 0, 0)
cannon_green = (0, 255, 0)
ball_colors = (red, blue, yellow, green, magenta, cyan)


class Game(Showable):
    def __init__(self, ball_target_color=ball_target_red, cannon_color=cannon_grey, cannon_charged_color=cannon_green,
                 cannon_fully_charged_color=cannon_red, colors=ball_colors):
        """
        Создаёт окно с игрой
        :param ball_target_color: цвет круглой мишени
        :param cannon_color: цвет пушки
        :param cannon_charged_color: цвет заряженной пушки
        :param cannon_fully_charged_color: цвет полностью заряженной пушки
        :param colors: список возможных цветов мячей
        """
        Showable.__init__(self)
        self.ball_target_color = ball_target_color
        self.ball_colors = colors
        self.cannon_color = cannon_color
        self.cannon_charged_color = cannon_charged_color
        self.cannon_fully_charged_color = cannon_fully_charged_color
        self.clock = pygame.time.Clock()
        self.finished = False
        self.score = 0
        self.game_finished = False

    def cannon_game(self):
        """
        Проводит игру "Пушка", возвращает номер меню окончания игры с подсчитанными очками
        """
        self.score = 0
        menu = menu_list[8]
        bullet_list = GameObjectsList()
        target_list = GameObjectsList()
        cannon = weapons.SimpleCannon(self.cannon_color, self.cannon_charged_color, self.cannon_fully_charged_color)
        for i in range(target_count):
            target_list.append(targets.BallTarget(self.ball_target_color))

        while not self.finished and not self.game_finished:
            menu.bg.blit()
            for group in group_list:
                group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cannon.charge()
                elif event.type == pygame.MOUSEBUTTONUP:
                    bullet_list.append(cannon.fire_ball(self.ball_colors))
                elif event.type == pygame.MOUSEMOTION:
                    cannon.targetting(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_finished = True

            cannon.config_sprite()
            for target in target_list:
                target.move()
            for ball in bullet_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target.kill()
                            target_list.pop(target_list.index(target))
                            target_list.append(targets.BallTarget(self.ball_target_color))
                            self.score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    bullet_list.smart_pop(0)
            cannon.power_up()
        for group in group_list:
            group.empty()
        num = 9
        menu_list[num].set_text('Your score is ' + str(self.score) + '!')
        return num

    def war_game(self):
        """
        Проводит игру "Война", возвращает номер меню окончания игры с подсчитанными очками
        """
        self.score = 0
        menu = menu_list[10]
        bullet_list = GameObjectsList()
        target_list = GameObjectsList()
        tank = weapons.Tank()
        for i in range(target_count):
            target_list.append(targets.BallTarget(self.ball_target_color))

        while not self.finished and not self.game_finished:
            menu.bg.blit()
            for group in group_list:
                group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    bullet_list.append(tank.fire_shell())
                elif event.type == pygame.MOUSEMOTION:
                    tank.targetting(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_finished = True
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        tank.add_left_speed()
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        tank.add_right_speed()
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        tank.add_right_speed()
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        tank.add_left_speed()

            tank.move()
            for target in target_list:
                target.move()
            for ball in bullet_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target.kill()
                            target_list.pop(target_list.index(target))
                            target_list.append(targets.BallTarget(self.ball_target_color))
                            self.score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    bullet_list.smart_pop(0)
        for group in group_list:
            group.empty()
        num = 11
        menu_list[num].set_text('Your score is ' + str(self.score) + '!')
        return num

    def hunt_game(self):
        """
        Проводит игру "Охота", возвращает номер меню окончания игры с подсчитанными очками
        """
        self.score = 0
        menu = menu_list[12]
        num = 13
        return num

    def minecraft_game(self):
        """
        Проводит игру "Minecraft", возвращает номер меню окончания игры с подсчитанными очками
        """
        self.score = 0
        menu = menu_list[14]
        num = 15
        return num

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.draw.rect(screen, (255, 255, 0), (100, 100, 200, 100))
        menu_number = 0  # номер текущего меню
        while not self.finished:
            game = None
            current_menu = menu_list[menu_number]
            current_menu.blit()
            pygame.display.update()
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                else:
                    if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                        i = current_menu.goto(event)
                        if i >= 0:
                            menu_number = i
                            current_menu = menu_list[menu_number]
                            if current_menu.game in ('Cannon', 'War', 'Hunt', 'Minecraft'):
                                game = current_menu.game
                                break
            if game == 'Cannon':
                menu_number = self.cannon_game()
            elif game == 'War':
                menu_number = self.war_game()
            elif game == 'Hunt':
                menu_number = self.hunt_game()
            elif game == 'Minecraft':
                menu_number = self.minecraft_game()
            self.game_finished = False
        pygame.quit()
        return self.score
