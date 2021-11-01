import pygame

from modules.buttons import ButtonGrid, Menu

button_text_color = (25, 12, 199)
menu_bg = 'menu_bg.jpg'

main_texts = ['Выбор режима', 'Горячие клавиши', 'Настройки']
choose_mode_texts = ['Пушка', 'Война', 'Охота', 'Minecraft']
hotkeys_texts = []
settings_texts = []
cannon_texts = []
war_texts = []
hunt_texts = []
minecraft_texts = []

main_links = [1, 2, 3]
choose_mode_links = [4, 5, 6, 7]
hotkeys_links = []
settings_links = []
cannon_links = []
war_links = []
hunt_links = []
minecraft_links = []

main_menu_text = ''
choose_mode_menu_text = ''
hotkeys_menu_text = 'Yet to be done...'
settings_menu_text = 'Yet to be done...'
cannon_menu_text = 'Yet to be done...'
war_menu_text = 'Yet to be done...'
hunt_menu_text = 'Yet to be done...'
minecraft_menu_text = 'Yet to be done...'

main_grid = ButtonGrid(button_text_color, 400, 200, main_texts)
choose_mode_grid = ButtonGrid(button_text_color, 400, 100, choose_mode_texts, back=True)
hotkeys_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
settings_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
cannon_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
war_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
hunt_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
minecraft_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)

main_menu = Menu(main_grid, main_links, main_menu_text, button_text_color, menu_bg)
choose_mode_menu = Menu(choose_mode_grid, choose_mode_links, choose_mode_menu_text, button_text_color, menu_bg, 0)
hotkeys_menu = Menu(hotkeys_grid, hotkeys_links, hotkeys_menu_text, button_text_color, menu_bg, 0, x=400, y=230)
settings_menu = Menu(settings_grid, settings_links, settings_menu_text, button_text_color, menu_bg, 0, x=400, y=230)
cannon_menu = Menu(cannon_grid, cannon_links, cannon_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
war_menu = Menu(war_grid, war_links, war_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
hunt_menu = Menu(hunt_grid, hunt_links, hunt_menu_text, button_text_color, menu_bg, 1, x=400, y=230)
minecraft_menu = Menu(minecraft_grid, minecraft_links, minecraft_menu_text, button_text_color, menu_bg, 1, x=400, y=230)

menu_list = [main_menu, choose_mode_menu, hotkeys_menu, settings_menu, cannon_menu, war_menu, hunt_menu, minecraft_menu]
