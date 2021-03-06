from modules.buttons import ButtonGrid
from modules.menu import Menu, GameMenu
from modules.vars import *

menu_bg = 'menu_bg.jpg'
cannon_bg = 'cannon_bg.jpg'
cannon_finish_bg = 'cannon_finish_bg.jpg'
war_bg = 'war_bg.jpg'
war_finish_bg = 'war_finish_bg.jpg'
war_lost_bg = 'war_lost_bg.jpg'
hunt_bg = 'hunt_bg.jpg'
hunt_finish_bg = 'hunt_finish_bg.jpg'
minecraft_bg = 'minecraft_bg.jpg'
minecraft_finish_bg = 'minecraft_finish_bg.jpg'
minecraft_lost_bg = 'minecraft_lost_bg.jpg'

main_texts = ['Выбор режима', 'Горячие клавиши', 'Настройки']
choose_mode_texts = ['Пушка', 'Война', 'Охота', 'Minecraft']
hotkeys_texts = []
settings_texts = []
cannon_texts = ['Играть']
war_texts = ['Играть']
hunt_texts = ['Играть']
minecraft_texts = ['Играть']
cannon_game_texts = []
cannon_score_texts = []
war_game_texts = []
war_score_texts = []
war_lose_texts = []
hunt_game_texts = []
hunt_score_texts = []
minecraft_game_texts = []
minecraft_score_texts = []
minecraft_lose_texts = ['Играть снова']

main_links = [1, 2, 3]
choose_mode_links = [4, 5, 6, 7]
hotkeys_links = []
settings_links = []
cannon_links = [8]
war_links = [10]
hunt_links = [13]
minecraft_links = [15]
cannon_game_links = []
cannon_score_links = []
war_game_links = []
war_score_links = []
war_lose_links = []
hunt_game_links = []
hunt_score_links = []
minecraft_game_links = []
minecraft_score_links = []
minecraft_lose_links = [15]

main_menu_text = ''
choose_mode_menu_text = ''
hotkeys_menu_text = 'Управляйте игрой левой кнопкой мыши\n\nESC - выход из игры\nA, D или <-, -> - управление танком'
settings_menu_text = 'Yet to be done...'
cannon_menu_text = 'Стреляйте по мячам из пушки!\n\nЧтобы выстрелить с максимальной силой,\nполностью зарядите пушку.\n' \
                   '(Когда пушка станвится красной - она заряжена.)'
war_menu_text = 'Уничтожьте вражеское укрепление, пока не поздно!\n\nПеремещайте танк клавишами <- и -> или A и D.\n' \
                'Не забывайте заранее сбивать истребители - \nпосле 5 попаданий их бомб вы погибнете!'
hunt_menu_text = 'Охотьтесь на диких животных,\nчтобы добыть ценные трофеи!\n\nПерезаряжайтесь кнопками Q или R.\n' \
                 'Не забывайте, что пули не бесконечные!'
minecraft_menu_text = 'Still in progress'
cannon_game_menu_text = ''
cannon_score_menu_text = ''
war_game_menu_text = ''
war_score_menu_text = 'Вы победили!'
war_lose_menu_text = 'Вы проиграли!'
hunt_game_menu_text = ''
hunt_score_menu_text = ''
minecraft_game_menu_text = ''
minecraft_score_menu_text = 'Still in progress'
minecraft_lose_menu_text = 'Дракон оказался сильнее...\nПопробуете ещё раз?'

main_grid = ButtonGrid(button_text_color, 400, 200, main_texts)
choose_mode_grid = ButtonGrid(button_text_color, 400, 100, choose_mode_texts, back=True)
hotkeys_grid = ButtonGrid(button_text_color, 400, 300, hotkeys_texts, back=True)
settings_grid = ButtonGrid(button_text_color, 400, 300, settings_texts, back=True)
cannon_grid = ButtonGrid(button_text_color, 400, 300, cannon_texts, back=True)
war_grid = ButtonGrid(button_text_color, 400, 300, war_texts, back=True)
hunt_grid = ButtonGrid(button_text_color, 400, 300, hunt_texts, back=True)
minecraft_grid = ButtonGrid(button_text_color, 400, 300, minecraft_texts, back=True)
cannon_game_grid = ButtonGrid(button_text_color, 250, -40, cannon_game_texts)
cannon_score_grid = ButtonGrid(button_text_color, 400, 400, cannon_score_texts, main=True)
war_game_grid = ButtonGrid(button_text_color, 250, -40, war_game_texts)
war_score_grid = ButtonGrid(button_text_color, 400, 400, war_score_texts, main=True)
war_lose_grid = ButtonGrid(button_text_color, 400, 400, war_lose_texts, main=True)
hunt_game_grid = ButtonGrid(button_text_color, 250, -40, hunt_game_texts)
hunt_score_grid = ButtonGrid(button_text_color, 400, 400, hunt_score_texts, main=True)
minecraft_game_grid = ButtonGrid(button_text_color, 250, -40, minecraft_game_texts)
minecraft_score_grid = ButtonGrid(button_text_color, 400, 400, minecraft_score_texts, main=True)
minecraft_lose_grid = ButtonGrid(button_text_color, 400, 330, minecraft_lose_texts, main=True)

main_menu = Menu(main_grid, main_links, main_menu_text, button_text_color, menu_bg)
choose_mode_menu = Menu(choose_mode_grid, choose_mode_links, choose_mode_menu_text, button_text_color, menu_bg, 0)
hotkeys_menu = Menu(hotkeys_grid, hotkeys_links, hotkeys_menu_text, button_text_color, menu_bg, 0, x=400, y=180)
settings_menu = Menu(settings_grid, settings_links, settings_menu_text, button_text_color, menu_bg, 0, x=400, y=230)
cannon_menu = Menu(cannon_grid, cannon_links, cannon_menu_text, button_text_color, menu_bg, 1, x=400, y=150)
war_menu = Menu(war_grid, war_links, war_menu_text, button_text_color, menu_bg, 1, x=400, y=150)
hunt_menu = Menu(hunt_grid, hunt_links, hunt_menu_text, button_text_color, menu_bg, 1, x=400, y=150)
minecraft_menu = Menu(minecraft_grid, minecraft_links, minecraft_menu_text, button_text_color, menu_bg, 1, x=400, y=230)

cannon_game_menu = GameMenu(cannon_game_grid, cannon_game_links, cannon_game_menu_text, button_text_color, cannon_bg, 4,
                            game='Cannon')
cannon_score_menu = Menu(cannon_score_grid, cannon_score_links, cannon_score_menu_text, cannon_finish_screen_color,
                         cannon_finish_bg, x=400, y=200, size=80, font=None)
war_game_menu = GameMenu(war_game_grid, war_game_links, war_game_menu_text, button_text_color, war_bg, 4, game='War')
war_score_menu = Menu(war_score_grid, war_score_links, war_score_menu_text, war_finish_screen_color,
                      war_finish_bg, x=400, y=200, line_gap=40, size=80, font=None)
war_lose_menu = Menu(war_lose_grid, war_lose_links, war_lose_menu_text, war_finish_screen_color,
                     war_lost_bg, x=400, y=250, size=80, font=None)
hunt_game_menu = GameMenu(hunt_game_grid, hunt_game_links, hunt_game_menu_text, button_text_color, hunt_bg, 4,
                          game='Hunt')
hunt_score_menu = Menu(hunt_score_grid, hunt_score_links, hunt_score_menu_text, hunt_finish_screen_color,
                       hunt_finish_bg, x=400, y=150, size=80, font=None)
minecraft_game_menu = GameMenu(minecraft_game_grid, minecraft_game_links, minecraft_game_menu_text, button_text_color,
                               minecraft_bg, 4, game='Minecraft')
minecraft_score_menu = Menu(minecraft_score_grid, minecraft_score_links, minecraft_score_menu_text,
                            minecraft_finish_screen_color, minecraft_finish_bg, x=400, y=200, size=80, font=None)
minecraft_lose_menu = Menu(minecraft_lose_grid, minecraft_lose_links, minecraft_lose_menu_text,
                           minecraft_lost_color, minecraft_lost_bg, x=400, y=200, line_gap=40, size=80, font=None)

menu_list = [main_menu, choose_mode_menu, hotkeys_menu, settings_menu, cannon_menu, war_menu, hunt_menu, minecraft_menu,
             cannon_game_menu, cannon_score_menu, war_game_menu, war_score_menu, war_lose_menu, hunt_game_menu,
             hunt_score_menu, minecraft_game_menu, minecraft_score_menu, minecraft_lose_menu]
