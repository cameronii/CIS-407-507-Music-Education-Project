"""
This is the main project file for the Vigenere Cipher Visualization and defines the main game loop
Authors: Joshua Fawcett, Max Hopkins, Meghan Riehl, Yuyao Zhuge

Citations:
Starter code for basic pygame window was pulled from:
https://www.geeksforgeeks.org/creating-start-menu-in-pygame/

Inspiration for class setup/scene managers:
https://nerdparadise.com/programming/pygame/part7
"""
import pygame
import sys
from SceneManager import *


FPS = 30

def main():

    # initializing the constructor
    pygame.init()
    #the starting menu
    scene = StartMenu()

    fpsClock = pygame.time.Clock()

    # screen resolution
    res = (1100, 800)

    # opens up a window
    screen = pygame.display.set_mode(res, pygame.RESIZABLE)

    active_scene = scene

    cursize = res

    while True:
        events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()
        for ev in events:

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.VIDEORESIZE:
                cursize = ev.size
                print(cursize)

        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        active_scene.Input(events, pressed_keys, mouse)
        active_scene.Render(screen, mouse)
        active_scene.update(screen, cursize)

        # if the scene is switched, this will load a new scene
        active_scene = active_scene.scene

        # updates the frames of the game
        pygame.display.update()

        fpsClock.tick(FPS)









if __name__ == "__main__":
    main()
