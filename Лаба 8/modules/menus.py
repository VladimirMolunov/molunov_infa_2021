import pygame

from modules.buttons import ButtonGrid, Menu, GameMenu

button_text_color = (25, 12, 199)
finish_screen_color = (6, 40, 17)
menu_bg = 'menu_bg.jpg'
bg = 'bg.jpg'
finish_bg = 'finish_bg.jpg'

main_texts = ['Выбор режима', 'Горячие клавиши', 'Настройки']
choose_mode_texts = ['Пушка', 'Война', 'Охота', 'Minecraft']
hotkeys_texts = []
settings_texts = []
cannon_texts = ['Играть']
war_texts = []
hunt_texts = []
minecraft_texts = []
score_texts = []
cannon_game_texts = []

main_links = [1, 2, 3]
choose_mode_links = [4, 5, 6, 7]
hotkeys_links = []
settings_links = []
cannon_links = [9]
war_links = []
hunt_links = []
minecraft_links = []
score_links = []
cannon_game_links = []

main_menu_text = ''
choose_mode_menu_text = ''
hotkeys_menu_text = 'ESC - выход из игры'
settings_menu_text = 'Yet to be done...'
cannon_menu_text = ''
war_menu_text = 'Yet to be done...'
hunt_menu_text = 'Yet to be done...'
minecraft_menu_text = 'Yet to be done...'
score_menu_text = 'h'
cannon_game_menu_text = ''

main_grid = ButtonGrid(button_text_color, 400, 200, main_texts)
choose_mode_grid = ButtonGrid(button_text_color, 400, 100, choose_mode_texts, back=True)
hotkeys_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
settings_grid = ButtonGrid(button_text_color, 400, 300, settings_texts, back=True)
cannon_grid = ButtonGrid(button_text_color, 400, 260, cannon_texts, back=True)
war_grid = ButtonGrid(button_text_color, 400, 300, war_texts, back=True)
hunt_grid = ButtonGrid(button_text_color, 400, 300, hunt_texts, back=True)
minecraft_grid = ButtonGrid(button_text_color, 400, 300, minecraft_texts, back=True)
score_grid = ButtonGrid(button_text_color, 400, 400, score_texts, main=True)
cannon_game_grid = ButtonGrid(button_text_color, 250, -40, cannon_game_texts)

main_menu = Menu(main_grid, main_links, main_menu_text, button_text_color, menu_bg)
choose_mode_menu = Menu(choose_mode_grid, choose_mode_links, choose_mode_menu_text, button_text_color, menu_bg, 0)
hotkeys_menu = Menu(hotkeys_grid, hotkeys_links, hotkeys_menu_text, button_text_color, menu_bg, 0, x=400, y=230)
settings_menu = Menu(settings_grid, settings_links, settings_menu_text, button_text_color, menu_bg, 0, x=400, y=230)
cannon_menu = Menu(cannon_grid, cannon_links, cannon_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
war_menu = Menu(war_grid, war_links, war_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
hunt_menu = Menu(hunt_grid, hunt_links, hunt_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
minecraft_menu = Menu(minecraft_grid, minecraft_links, minecraft_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
score_menu = Menu(score_grid, score_links, score_menu_text, finish_screen_color, finish_bg, x=400, y=200, size=80,
                  font=None)
cannon_game_menu = GameMenu(cannon_game_grid, cannon_game_links, cannon_game_menu_text, button_text_color, bg, 4,
                            game='Cannon')

menu_list = [main_menu, choose_mode_menu, hotkeys_menu, settings_menu, cannon_menu, war_menu, hunt_menu, minecraft_menu,
             score_menu, cannon_game_menu]
