import pygame
"""
This file defines the button() class, which is used to render buttons, the text on the buttons,
and define their functionality.
"""
class button():
    """
    Use this class to define buttons in the scene
    """
    def __init__(self, y1, text, click_funct, x1=5, x2=150, y2=30, textOffsetx = 5, textOffsety = 5,
                 color_light = (170, 170, 170), color_dark = (100, 100, 100)):
        """
        y1: position of the button origin on the y coordinate
        text: text to be displayed onto the button. Should be a rendered font
        click_funct: The function that is called when the button is clicked
        x1: the position of the button origin on the x coordinate
        textOffsetx: the position of the text away from the button origin on the x coordinate
        textOffsety: the position of the text away from the button origin on the y coordinate
        color_light: the color that is displayed when the button is being hovered on
        color_dark: default color of the button
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.textOffsetx = textOffsetx
        self.textOffsety = textOffsety
        self.text = text
        self.click_funct = click_funct
        self.color_light = color_light
        self.color_dark = color_dark

    def draw(self, screen):
        """
        draws the button rectangle and the button text onto the scene
        """
        if self.hover(pygame.mouse.get_pos()):
            # print(self.text, self.x1, self.x2, self.y1, self.y2)
            pygame.draw.rect(screen, self.color_light, [self.x1, self.y1, self.x2, self.y2])
        else:
            # print(self.text, self.x1, self.x2, self.y1, self.y2)
            pygame.draw.rect(screen, self.color_dark, [self.x1, self.y1, self.x2, self.y2])
        screen.blit(self.text, (self.x1 + self.textOffsetx, self.y1 + self.textOffsety))

    def hover(self, mouse):
        """
        When the mouse is over the button, change the color
        """
        if self.x1 <= mouse[0] <= (self.x1 + self.x2) and self.y1 <= mouse[1] <= (self.y1 + self.y2):
            return True
        else:
            return False

    def click(self):
        """
        When the button is clicked on, call this function
        """
        self.click_funct()