import math
import pygame
from pathlib import Path

from modules import bullets, weapons, targets
from modules.buttons import Menu
from modules.menus import menu_list
from modules.groups import group_list
from modules.classes import Showable, GameObjectsList, Background
from modules.vars import *


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
                    if event.button == 1:
                        cannon.charge()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
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
                            target_list.smart_pop(target_list.index(target))
                            target_list.append(targets.BallTarget(self.ball_target_color))
                            self.score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    bullet_list.smart_pop(bullet_list.index(ball))
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
        won = False
        self.score = 0
        menu = menu_list[10]
        bullet_list = GameObjectsList()
        enemy_bullet_list = GameObjectsList()
        target_list = GameObjectsList()
        plane_list = GameObjectsList()
        tank = weapons.Tank()
        for i in range(target_count):
            target_list.append(targets.BallTarget(self.ball_target_color, health=6, show_healthbar=True))

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
                    if event.button == 1:
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
            if len(plane_list) < plane_count:
                plane_list.append(targets.Plane())
            for plane in plane_list:
                plane.move()
                if 0 < (plane.x - tank.x) < 200:
                    if plane.check_charge():
                        enemy_bullet_list.append(plane.fire_bomb())
                if plane.x < -plane.width:
                    plane_list.smart_pop(plane_list.index(plane))
            for target in target_list:
                target.move()
            for bomb in enemy_bullet_list:
                bomb.move()
                if bomb.is_hit(tank) and tank.health > 0:
                    bomb.live = 0
                    tank.hit()
                    if tank.health == 0:
                        tank.kill()
                        self.game_finished = True
                bomb.remove_life()
                if bomb.live <= 0:
                    enemy_bullet_list.smart_pop(enemy_bullet_list.index(bomb))

            for shell in bullet_list:
                shell.move()
                for target in target_list:
                    if shell.is_hit(target) and target.health > 0:
                        shell.live = 0
                        target.hit()
                        if target.health == 0:
                            target_list.smart_pop(target_list.index(target))
                            target_list.append(targets.BallTarget(self.ball_target_color, health=6,
                                                                  show_healthbar=True))
                            self.score += score_for_catch
                        break
                for plane in plane_list:
                    if shell.is_hit(plane) and plane.health > 0:
                        shell.live = 0
                        plane.hit()
                        if plane.health == 0:
                            target_list.smart_pop(target_list.index(plane))
                            target_list.append(targets.BallTarget(self.ball_target_color, health=6,
                                                                  show_healthbar=True))
                            self.score += score_for_catch
                        break
                shell.remove_life()
                if shell.live <= 0:
                    bullet_list.smart_pop(bullet_list.index(shell))
        for group in group_list:
            group.empty()
        if won:
            num = 11
            menu_list[num].add_text('Your score is ' + str(self.score) + '.')
        else:
            num = 12
        return num

    def hunt_game(self):
        """
        Проводит игру "Охота", возвращает номер меню окончания игры с подсчитанными очками
        """
        self.score = 0
        menu = menu_list[13]
        bullet_list = GameObjectsList()
        target_list = GameObjectsList()
        gun = weapons.Gun()
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
                    if event.button == 1:
                        bullet_list.append(gun.fire_ball(self.ball_colors))
                elif event.type == pygame.MOUSEMOTION:
                    gun.targetting(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_finished = True

            gun.move()
            for target in target_list:
                target.move()
            for ball in bullet_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target_list.smart_pop(target_list.index(target))
                            target_list.append(targets.BallTarget(self.ball_target_color))
                            self.score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    bullet_list.smart_pop(bullet_list.index(ball))
        for group in group_list:
            group.empty()
        num = 14
        menu_list[num].set_text('Your score is ' + str(self.score) + '!')
        return num

    def minecraft_game(self):
        """
        Проводит игру "Minecraft", возвращает номер меню окончания игры с подсчитанными очками
        """
        self.score = 0
        menu = menu_list[15]
        bullet_list = GameObjectsList()
        target_list = GameObjectsList()
        tank = weapons.Tank()
        for i in range(1):
            target_list.append(targets.Dragon())
        time = pygame.time.get_ticks()

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
                    if event.button == 1:
                        bullet_list.append(tank.fire_shell())
                elif event.type == pygame.MOUSEMOTION:
                    tank.targetting(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_finished = True
                        time = -1
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
            for dragon in target_list:
                dragon.move()
            for shell in bullet_list:
                shell.move()
                for dragon in target_list:
                    if shell.is_hit(dragon) and dragon.health > 0:
                        shell.live = 0
                        dragon.hit()
                        if dragon.health == 0:
                            dragon.kill()
                            time = round((pygame.time.get_ticks() - time) / 100) / 10
                            self.game_finished = True
                        break
                shell.remove_life()
                if shell.live <= 0:
                    bullet_list.smart_pop(bullet_list.index(shell))
        for group in group_list:
            group.empty()
        if time == -1:
            num = 17
        else:
            num = 16
            menu_list[num].set_text('Your time is ' + str(time) + ' s!')
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

