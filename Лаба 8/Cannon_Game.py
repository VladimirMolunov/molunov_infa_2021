from modules.game import Game

red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
magenta = (255, 3, 184)
cyan = (0, 255, 204)
white = (255, 255, 255)
grey = (102, 102, 102)
target_red = (228, 0, 0)
gun_red = (255, 0, 0)
gun_green = (0, 255, 0)
ball_colors = [red, blue, yellow, green, magenta, cyan]


def main():
    mygame = Game(target_red, grey, gun_green, gun_red, ball_colors)
    mygame.main()


if __name__ == "__main__":
    main()
