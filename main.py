import pygame
import pygame_menu
import os
import src.gameengine  

def set_difficulty(value, difficulty):
    pass

def start_the_game():
    # Initialize the game engine and run the game
    joc = src.gameengine.GameEngine(1200, 800)
    joc.run()

pygame.init()

surface = pygame.display.set_mode((800, 600))

custom_theme = pygame_menu.themes.Theme(background_color=(0, 255, 0, 0), title_font=pygame_menu.font.FONT_8BIT, title_font_size=30, widget_font=pygame_menu.font.FONT_8BIT, widget_font_size=20)
background_image = pygame_menu.baseimage.BaseImage(os.path.normpath('src/assets/sprites/tiles/bkg.png'))
custom_theme.background_color = background_image

menu = pygame_menu.Menu('Petru Griffon x Ghiu Simulator', 800, 600, theme=custom_theme)

menu.add.text_input('Name', font_color=(255, 255, 255))

menu.add.selector('Difficulty', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty, font_color=(255, 255, 255))

menu.add.button('Play', start_the_game, font_color=(255, 255, 255))
menu.add.button('Quit', pygame_menu.events.EXIT, font_color=(255, 255, 255))

# Run the menu loop
menu.mainloop(surface)
