import pygame
from button_class import button
from main import FPS

"""
This is where scenes are defined for the Visualization tool
Authors: Joshua Fawcett, Max Hopkins, Meghan Riehl, Yuyao Zhuge 
"""

class SceneManager:
    """
    Base class for all scenes, defines functions that all scenes can use
    """
    def __init__(self):
        self.scene = self

    def Input(self, events, pressed_keys, mouse):
        """
        Reads input and updates variables based on input
        :param events: a list of events that has happened since last frame update
        :param pressed_keys: the list of pressed keys since the last frame update
        :param mouse: the position of the mouse
        :return: none
        """
        print("Input not overridden")

    def Render(self, screen, mouse):
        """
        Renders text and shapes onto screen
        :param screen: the initialized screen
        :param mouse: the position of the mouse
        :return: none
        """
        print("Render not overriden")

    def update(self, screen, cursize):
        """
        Updates variables each frame, mainly used to reposition items after a resize
        :param screen: the initialized screen
        :param cursize: the size of the screen
        :return: none
        """
        return None

    def SwitchToScene(self, next_scene):
        """
        Updates self.scene to load the next scene
        :param next_scene: the scene that should be displayed after this funciton is called.
        :return:
        """
        self.scene = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


'''
class ButtonScene(SceneManager):
    """
    The scene for the visualization of the algorithm. Includes the table and the controls.
    """
    def __init__(self, message, key, result, steps, mode):
        """

        :param message: the message input by the user
        :param key: the key input by the user
        :param result: the result of the encryption/decryption process
        :param steps: a tuple of the steps from the cipher
        :param mode: can either be encryption=0 or decryption=1
        """
        SceneManager.__init__(self)

        # self.table holds an instance of the Table class from the table module. This variable is responsible for drawing
        # and updating the vigenere table that is shown when encrypting/decrytping. It is used specifically
        # in self.update() and self.displayBoard()
        self.table = Table()

        # self.displayText is an instance of the Text_And_Highlight class from the TextHighlight module. This variable
        # is responsible for displaying and updating the message/keyword/result text when encrypting/decrypting. It is used
        # in self.displayBoard() and self.Render()
        self.displayText = Text_And_Highlight()

        # self.result is a string that holds the correctly encrypted/decrypted text from the cipher module. 
        self.result = result

        # self.steps is a list of the form [(r1, c1), (r2, c2), ...], which represent the indices into the rows and columns
        # of the vigenere table. The steps are used by the self.table in order to highlight the correct row and column for
        # each step in the visualization
        self.steps = steps

        # self.mode is an integer value representing the current mode of operation. It can either be 0 for encryption or
        # 1 for decryption. It is used in self.displayBoard() in order to make the correct highlight function calls for
        # self.table and self.displayText
        self.mode = mode

        # self.message is a string that holds the message that the user entered for encryption/decryption. This variable is used
        # by self.displayText to display the message to the screen while encrypting/decrypting
        self.message = message

        # self.key is a string that holds the keyword that the user entered for encryption/decryption. This variable is used
        # by self.displayText to display the keyword to the screen while encrypting/decrypting
        self.key = key

        # self.pace is a variable that holds the current pace that the user sets. It has a minimum value of 1 and a maximum
        # value of 10. The default value always starts at 5. 
        self.pace = 5

        # self.updateSpeed is a variable that represents how many times the visualization updates itself per second when in
        # play mode. Its value is based on the current pace set by the user, and is used in self.update() to determine when
        # the next step in the visualization will be displayed. FPS is declared in the main module and basically represents
        # the number of times that pygame draws the screen for every second. The default update speed will be the same as the
        # FPS, meaning that the visualization will update once per second. This value is updated on the "speed up" and "slow down"
        # button presses by the user
        self.updateSpeed = (FPS // self.pace) * 5

        # self.paused keeps track of the current state of the visualization. A value of false means the visualization is playing, while
        # a value of true means the visualization is paused. This value is used in self.update() and is updated by the "paused"/"play"
        # button presses
        self.paused = False # Used to pause the game

        # self.mainSurfaceSize is a variable that holds the current size of the actual display surface in main. It is used to handle
        # functionality for when the user resizes the window of the application. This value is updated in self.update()
        self.mainSurfaceSize = (0, 0)

        # self.mainDislay holds a reference to the actual display surface in main. This variable is used to copy all of the local display
        # changes (drawing buttons, vigenere table, display text, highlights, etc) over the actual display surface that is seen by the user.
        # This variable is initialized with a random surface and is immediately overwritten on the first call to self.update()
        self.mainDisplay = pygame.Surface((1, 1))

        # self.ind is an integer that holds the index of the next step to be displayed in self.steps. It is used mainly in
        # self.displayBoard() to display the next step in the visualization. 
        self.ind = 0

        # self.timer is a varaible that is used in self.update() to determine when the next update will happen. The timer is incremented
        # once per frame (once every time self.update is called in the main game loop in the main module)
        self.timer = 0

        # white color
        self.color = (255, 255, 255)
        #dark grey
        self.color_dark = (100, 100, 100)
        #Green colors for play button
        self.light_green = (0, 204, 0)
        self.dark_green =(0, 102, 0)

        #Red colors for paused button
        self.light_red = (255, 102, 102)
        self.dark_red = (153, 0, 0)

        # defining a font
        self.smallfont = pygame.font.SysFont('Corbel', 25)
        self.font = pg.font.SysFont("FreeSans", 28, bold=True)

        # rendering a text written in this font
        self.menu = self.smallfont.render('Go Back', True, self.color)
        self.play = self.smallfont.render('Playing', True, self.color)
        self.pause = self.smallfont.render('Paused', True, self.color)
        self.forw = self.smallfont.render('Step Forward', True, self.color)
        self.back = self.smallfont.render('Step Back', True, self.color)
        self.up = self.smallfont.render('Speed Up', True, self.color)
        self.down = self.smallfont.render('Slow Down', True, self.color)
        self.res = self.smallfont.render('Restart', True, self.color)
        self.encryptText = self.font.render('Encrypting', True, self.color_dark)
        self.decryptText = self.font.render('Decrypting', True, self.color_dark)
        self.PlayPause = self.play

    # Updates the self.updateSpeed variable so the self.update() function makes update
    # to the board at the appropriate rate
    def updatePace(self):
        self.updateSpeed = (FPS // self.pace) * 5
        return None


    # This function makes the animation play slower. It is called on the 'slow down'
    # button presses by the user
    def slowDown(self):
        if (self.pace > 1): # Minimum pace is 1

            # decrement the current pace
            self.pace -= 1

            # update the 'self.updateSpeed' variable with this function call. Having
            # a separate function may be unecessary for this but it works. 
            self.updatePace()
        return None

    # This function makes the animation play faster. It is called on the 'speed up'
    # button presses by the user
    def speedUp(self):
        if (self.pace < 10): # Max pace is 10

            # increment the current pace
            self.pace += 1

            # update the 'self.updateSpeed' variable with this function call. Having
            # a separate function may be unecessary for this but it works. 
            self.updatePace()
        return None

    # This function displays the previous step in the animation. It can only
    # be called if the animation is currently paused. It is called on the 'step back'
    # button presses by the user.
    def stepBack(self):
        if (self.paused): # if the animation is currently paused

            # since self.ind generally points to the next step to be shown, the index needs to be
            # decremented by 2 in order to get the previous step. 
            self.ind = (self.ind - 2) % len(self.steps)

            # display the previous step in the animation
            self.displayBoard(self.ind)

            # increment the index in order to point to the next step to be played
            self.ind = (self.ind + 1) % len(self.steps)
        return None

    # This function displays the next sequential step in the animation. It can only
    # be called if the animation is currently paused. It is called on the 'step forward'
    # button presses by the user.
    def stepForward(self):
        if (self.paused): # if the animation is currently paused

            self.displayBoard(self.ind) # display the next step in the animation
            
            self.ind = (self.ind + 1) % len(self.steps) # increment the index
        return None

    # This function stops the current animation process and starts it over from the
    # first step. It is called on the 'restart' button presses by the user
    def restart(self):
        # pause the animation so it can't continue to play while it is being reset
        self.paused = True

        # Clear the table of any highlights with the table.refresh method
        self.table.refresh()

        # Call self.displayBoard to show the very first step in the animation
        self.displayBoard(0)

        # Reset the current instruction index
        self.ind = 1

        # Could possibly have something like "self.paused = False" if we want the animation
        # to start playing automatically after it has been reset. For now the animation stays paused
        # after resetting and the user has to click 'play' in order to resume the visualization
        return None

    # Toggles the value of the self.pause variable. This is called on the
    # 'pause'/'play' button presses by the user. A value of true pauses the visualization,
    # and a value of false resumes/plays the animation. 
    def togglePause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def Input(self, events, pressed_keys, mouse):
        for ev in events:
            """
            if ev.type == pygame.QUIT:
                pygame.quit()
            """
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on a
                # button the game does the thing
                for i in self.buttons:
                    if i.hover(mouse):
                        i.click()

    def Render(self, screen, mouse):
        #screen.fill((255, 255, 165))
        #updates the speed multiplier display
        self.speed = f"Speed: {self.pace}X"
        self.speedText = self.font.render(self.speed, True, self.color_dark)


        # defining buttons
        # and their locations
        if self.paused:
            self.PlayPause = self.pause
            play_button = button(40, self.PlayPause, lambda: self.togglePause(), color_light=self.light_red,
                                 color_dark=self.dark_red)
        else:
            self.PlayPause = self.play
            play_button = button(40, self.PlayPause, lambda: self.togglePause(), color_light=self.light_green,
                                 color_dark=self.dark_green)

        forw_button = button(85, self.forw, lambda: self.stepForward())
        back_button = button(120, self.back, lambda: self.stepBack())
        up_button = button(165, self.up, lambda: self.speedUp())
        down_button = button(200, self.down, lambda: self.slowDown())
        res_button = button(245, self.res, lambda: self.restart())
        menu_button = button(280, self.menu, lambda: self.SwitchToScene(MainMenu()))

        self.buttons = [menu_button, play_button, forw_button, back_button, up_button, down_button,
                        res_button]

        self.mainDisplay.blit(self.displayText.screen, (0, 500))
        self.displayText.write_letter(self.message.upper(), self.key.upper(), self.result.upper(), self.mode)

        #draw buttons
        for i in self.buttons:
            i.draw(screen)

        #if we are encrypting, display encryptText
        if self.mode == 0:
            screen.blit(self.encryptText, (5, 5))
        #if we are decrypting, display decryptText
        elif self.mode == 1:
            screen.blit(self.decryptText, (5, 5))
        #display the speed multiplier
        screen.blit(self.speedText, (5, 315))

        #screen.blit(self.messageText, (5, 285))
        #screen.blit(self.message, (5, 305))
        #screen.blit(self.keyText, (5, 345))
        #screen.blit(self.key, (5, 365))
        #screen.blit(self.resultText, (5, 405))
        #screen.blit(self.result, (5, 425))

    # This function handles all functionality related to updating the table display for the scene.
    # The argument 'index' refers to an index into the instruction list, so that the correct
    # rows and columns get highlighted
    def displayBoard(self, index):
        # Fill the screen with a yellowish background. Probably not the best to completely refill
        # the background on every update. It might be better to fill the background on initialization
        # in order to cover the previous scene. But this works for now.
        self.mainDisplay.fill((255, 255, 165))

        # Redraw the buttons and message/keyword/result every update because they are covered by the
        # previous line which fills the entire screen. 
        self.Render(self.mainDisplay, None)

        # Change table position based on screen size. If main screen size changes, the table will align itself
        # to the very right edge of the screen to make as much room for the buttons and message/keyword/result text
        # as possible. Not sure what happens when screen size is smaller than the table size 
        x = (self.mainBoardSize[0] / 2) - 300
        
        if (self.mode == 0): # if current mode is encryption
            # Call table.displayEncrypt
            self.table.displayEncrypt(self.steps[index][1], self.steps[index][0])
        else: # if current mode is decryption
            # Call table.displayDecrypt
            self.table.displayDecrypt(self.steps[index][1], self.steps[index][0])

        #Highlight the correct letters in the display text
        self.displayText.highlight(index, self.mode)

        # blit (copy) the table onto the main button scene display at the correct position
        self.mainDisplay.blit(self.table.screen, (x, 10))
        return None

    # This function is called once per game loop in the main.py file. It adds functionality
    # for updating the screen at a certain pace
    def update(self, board, size):
        self.mainBoardSize = size # update the board size variable to match the actual screen size
        self.mainDisplay = board # update the main display surface variable
        x = (self.mainBoardSize[0] / 2) - 300 # Find new position for table based on screen size
        self.mainDisplay.fill((255, 255, 165)) # fill background with yellow color

        self.Render(self.mainDisplay, None) # Render all of the buttons and the display Text
        self.mainDisplay.blit(self.table.screen, (x, 10)) # draw the table to the screen
        
        if (not self.paused): # if the game is paused, the board should not update

            if (self.timer == 0): # every time the timer == 0, the board updates

                # Call the display board funtion which handles all of the functionality
                # for actually displaying the updates to the board
                self.displayBoard(self.ind)

                # Increment the instruction index. Modulo for wrap around, so the animation
                # plays on repeat
                self.ind = (self.ind + 1) % len(self.steps)
                
            # Increment the timer using modulo, so whenever (timer + 1) == updateSpeed,
            # the result of modulo division will be 0, and the board will update
            self.timer = (self.timer + 1) % self.updateSpeed
        return None
'''
class MainMenu(SceneManager):
    """
    This is the class for the menu where the user enters their message/key
    """
    def __init__(self):
        SceneManager.__init__(self)
        # white color
        self.color = (255, 255, 255)

        # light shade of the button
        self.color_light = (170, 170, 170)

        # dark shade of the button
        self.color_dark = (100, 100, 100)

        # Dark red for error message
        self.color_darkred = (55, 0, 0)

        # stores the width of the
        # screen into a variable
        self.width = 720

        # stores the height of the
        # screen into a variable
        self.height = 720

        # defining a font
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.input_smallfont = pygame.font.SysFont('Corbel', 24)

        # rendering a text written in
        # this font
        self.encrypt = self.smallfont.render('encrypt', True, self.color)
        self.decrypt = self.smallfont.render('decrypt', True, self.color)
        self.message = self.smallfont.render("message", True, self.color_dark)
        self.key = self.smallfont.render("key", True, self.color_dark)
        self.title = self.smallfont.render("Vigenere Visualization Tool", True, self.color_dark)
        self.error_message = self.smallfont.render("Error: please input a valid key/message", True, self.color_darkred)
        self.menu = self.smallfont.render('Back to Main Menu', True, self.color)


        # Error boolean
        self.error = False

        #Defining colors
        self.message_color = self.color
        self.key_color = self.color

        #Booleans for switching between inputs
        self.message_active = False
        self.key_active = False

        #sent to ButtonScene, updates when the user inputs letters
        self.message_text = ''
        self.key_text = ''

        #A list of valid characters that can be input
        self.validCharacters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']

    def Input(self, events, pressed_keys, mouse):
        for ev in events:
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #check all buttons, if the mouse is hovering over it on this event, trigger click()
                for i in self.buttons:
                    if i.hover(mouse):
                        i.click()

                # if the mouse is clicked on the Encryption button, load button scene if input is valid
                if self.encrypt_rect.collidepoint(ev.pos):
                    pygame.quit()

                # if the mouse is clicked on the Decryption button, load button scene if input is valid
                if self.decrypt_rect.collidepoint(ev.pos):
                    pygame.quit()

                #the input bar for the message, will deactivate when key input bar is activated
                if self.message_rect.collidepoint(ev.pos):
                    self.message_active = True
                    self.message_color = self.color_light
                    self.key_color = self.color
                    self.key_active = False

                #the input bar for the key, will deactivate when message input bar is activated
                if self.key_rect.collidepoint(ev.pos):
                    self.key_active = True
                    self.key_color = self.color_light
                    self.message_color = self.color
                    self.message_active = False

            if ev.type == pygame.KEYDOWN:
                #if the user has selected the message bar to type into, display on screen and update message_text
                if self.message_active:
                    #delete a character if backspace is pressed
                    if ev.key == pygame.K_BACKSPACE:
                        self.message_text = self.message_text[:-1]
                    #check if valid input/not too long
                    elif ev.unicode in self.validCharacters and len(self.message_text) <= 19:
                        self.message_text += ev.unicode

                #if the user has selected the key bar to type into, display on screen and update key_text
                elif self.key_active:
                    #delete a character if backspace is pressed
                    if ev.key == pygame.K_BACKSPACE:
                        self.key_text = self.key_text[:-1]
                    #check if valid input/not too long
                    elif ev.unicode in self.validCharacters and len(self.key_text) <= 19:
                        self.key_text += ev.unicode

    def Render(self, screen, mouse):
        # fills the screen with a color
        screen.fill((255, 255, 165))

        pygame.draw.rect
        #define the encrypt button here to update the position if screen size changes
        self.encrypt_rect = pygame.Rect(self.width / 2 + 50, self.height / 1.7, 140, 40)
        #define the decrypt button here to update the position if screen size changes
        self.decrypt_rect = pygame.Rect(self.width / 2 - 200, self.height / 1.7, 140, 40)
        #define the message input rect here to update the position if screen size changes
        self.message_rect = pygame.Rect(self.width / 2 - 150, self.height / 4.2, 300, 40)
        # define the key input rect here to update the position if screen size changes
        self.key_rect = pygame.Rect(self.width / 2 - 150, self.height / 2.5, 300, 40)
        #The menu button to return to the main menu is defined hre to update position
        menu_button = button(self.height / 1.3, self.menu, lambda: self.SwitchToScene(StartMenu()), self.width / 2 - 140,
                             280, 40)
        #the list of buttons in our scene
        self.buttons = [menu_button]
        #draw all buttons in the scene
        for i in self.buttons:
            i.draw(screen)

        # if mouse is hovered over encrypt it
        # changes to lighter shade
        if self.width / 2 + 50 <= mouse[0] <= self.width / 2 + 50 + 140 and self.height / 1.7 <= mouse[1] <= self.height / 1.7 + 40:
            pygame.draw.rect(screen, self.color_light, self.encrypt_rect)

        else:
            pygame.draw.rect(screen, self.color_dark, self.encrypt_rect)

        # if mouse is hovered over decrypt it
        # changes to lighter shade
        if self.width / 2 - 200 <= mouse[0] <= self.width / 2 - 200 + 140 and self.height / 1.7 <= mouse[1] <= self.height / 1.7 + 40:
            pygame.draw.rect(screen, self.color_light, self.decrypt_rect)

        else:
            pygame.draw.rect(screen, self.color_dark, self.decrypt_rect)

        #the user's input is being defined as a font so that it can be displayed to the screen
        message_input = self.input_smallfont.render(self.message_text, True, self.color_dark)
        key_input = self.input_smallfont.render(self.key_text, True, self.color_dark)

        #Draw the input rectangles that we defined earlier
        pygame.draw.rect(screen, self.message_color, self.message_rect)
        pygame.draw.rect(screen, self.key_color, self.key_rect)

        # superimposing text onto our buttons
        screen.blit(self.encrypt, (self.encrypt_rect.x + 10, self.encrypt_rect.y))
        screen.blit(self.decrypt, (self.decrypt_rect.x + 10, self.decrypt_rect.y))
        screen.blit(self.message, (self.width / 2 - 60, self.height / 3.5))
        screen.blit(self.key, (self.width / 2 - 30, self.height / 2.2))
        screen.blit(self.title, (self.width / 2 - 200, self.height / 8))
        screen.blit(message_input, (self.message_rect.x + 10, self.message_rect.y + 10))
        screen.blit(key_input, (self.key_rect.x + 10, self.key_rect.y + 10))
        #if there is invalid input, display an error message
        if self.error:
            screen.blit(self.error_message, (self.width / 2 - 275, self.height / 1.5))

    # This function is used to update the screen size to reposition objects in our scene
    def update(self, board, size):
        self.width = size[0]
        self.height = size[1]

class StartMenu(SceneManager):
    """
    The first menu that is displayed when the program starts.
    Defines 3 buttons:
        1. Visualization button: loads MainMenu() for the user to use the visualization tool
        2. Info button: loads InfoMenu() for the user to learn about the system
        3. Quit: quits the program
    """
    def __init__(self):
        SceneManager.__init__(self)
        # white color
        self.color = (255, 255, 255)

        # light shade of the button
        self.color_light = (170, 170, 170)

        # dark shade of the button
        self.color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        self.width = 1100

        # stores the height of the
        # screen into a variable
        self.height = 800

        # defining a font
        self.importantfont = pygame.font.SysFont('Corbel', 45, bold=True)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.input_smallfont = pygame.font.SysFont('Corbel', 24)

        # rendering a text written in
        # this font
        self.title = self.smallfont.render("Vigenere Visualization Tool", True, self.color_dark)
        self.menu = self.smallfont.render('Visualization Tool', True, self.color)
        self.info = self.smallfont.render('Info', True, self.color)
        self.quit = self.smallfont.render('Quit', True, self.color)
        self.important = self.importantfont.render("Best used in fullscreen!", True, self.color_dark)
        self.buttons = []


    def Input(self, events, pressed_keys, mouse):
        for ev in events:
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # if mouse is clicked while hovering over a button, call the click() function
                for i in self.buttons:
                    if i.hover(mouse):
                        i.click()


    def Render(self, screen, mouse):
        # fills the screen with a color
        screen.fill((255, 255, 165))

        pygame.draw.rect
        #buttons defined here to update when screen changes size
        menu_button = button(self.height / 4.2, self.menu, lambda: self.SwitchToScene(MainMenu()), self.width / 2 - 140,
                             250, 40)
        info_button = button(self.height / 2.7, self.info, lambda: pygame.quit(), self.width / 2 - 140,
                             250, 40, 100)
        quit_button = button(self.height / 2, self.quit, lambda: pygame.quit(), self.width / 2 - 140, 250, 40, 100)
        self.buttons = [menu_button, info_button, quit_button]
        #draw all buttons in the scene
        for i in self.buttons:
            i.draw(screen)
        #render our title and fullscreen suggestion
        screen.blit(self.title, (self.width / 2 - 200, self.height / 8))
        screen.blit(self.important, (self.width / 2 - 225, self.height / 1.5))

    def update(self, screen, cursize):
        self.width = cursize[0]
        self.height = cursize[1]
'''
class InfoMenu(SceneManager):
    """
    This is our main information menu, which defines three buttons:
        1. About ciphers button: When clicked, it will load the scene About(), which displays info about ciphers
        2. About this tool: When clicked, it will load the scene Use(), which displays how to use the tool
        3. Go back button: When clicked, it will load the scene StartMenu(), taking you back to the main screen
    """
    def __init__(self):
        SceneManager.__init__(self)

        # white color
        self.color = (255, 255, 255)

        # light shade of the button
        self.color_light = (170, 170, 170)

        # dark shade of the button
        self.color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        self.width = 720

        # stores the height of the
        # screen into a variable
        self.height = 720


        # defining a font
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.input_smallfont = pygame.font.SysFont('Corbel', 24)

        # rendering a text written in
        # this font
        self.about = self.smallfont.render('About Ciphers', True, self.color)
        self.use = self.smallfont.render('About This Tool', True, self.color)
        self.menu = self.smallfont.render("Go Back", True, self.color)
        self.information = self.smallfont.render("Information", True, self.color_dark)

    def Input(self, events, pressed_keys, mouse):
        for ev in events:
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on a
                # button the game does the thing
                for i in self.buttons:
                    if i.hover(mouse):
                        i.click()

    def Render(self, screen, mouse):
        # fills the screen with a color
        screen.fill((255, 255, 165))
        # buttons and their locations/functions
        about_button = button(self.height / 4.7, self.about, lambda: self.SwitchToScene(About()),
                              self.width / 2 - 140,
                              250, 40, 30)
        use_button = button(self.height / 2.8, self.use, lambda: self.SwitchToScene(Use()), self.width / 2 - 140,
                            250, 40, 20)

        menu_button = button(self.height / 2, self.menu, lambda: self.SwitchToScene(StartMenu()),
                             self.width / 2 - 140,
                             250, 40, 70)

        self.buttons = [menu_button, about_button, use_button]
        #draw all defined buttons into the scene
        for i in self.buttons:
            i.draw(screen)

        #Menu title
        screen.blit(self.information, (self.width / 2 - 100, self.height / 8))

    def update(self, board, size):
        self.width = size[0]
        self.height = size[1]

class Use(SceneManager):
    """
    This menu loads when the user selects the "About this tool" button in InfoScene()
    This scene informs the user on how to use the tool, and what the control buttons do
    It defines 2 buttons:
        1. Main Menu: this will load the StartMenu() scene, taking the user back to the main menu
        2. Cipher information: This will load the About() scene, flipping the user between the two main info scenes
    """
    def __init__(self):
        SceneManager.__init__(self)
        #print("Information")

        # white color
        self.color = (255, 255, 255)

        # light shade of the button
        self.color_light = (170, 170, 170)

        # dark shade of the button
        self.color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        self.width = 720

        # stores the height of the
        # screen into a variable
        self.height = 720
        # defining a font
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.titlefont = pygame.font.SysFont('Corbel', 50, bold = True)
        self.heading = pygame.font.SysFont('Corbel', 35, bold = True)
        self.controls = pygame.font.SysFont('Corbel', 26, bold = True, italic = True)
        self.smallerfont = pygame.font.SysFont('Corbel', 30)
        self.input_smallfont = pygame.font.SysFont('Corbel', 24)

        # rendering button and title text
        self.menu = self.smallfont.render("Main Menu", True, self.color)
        self.other = self.smallfont.render("Cipher Information", True, self.color)
        self.title = self.titlefont.render("Using this tool", True, self.color_dark)

        # rendering information text
        self.text1 = self.smallerfont.render("This tool is a visualization of the Vigenere cipher, it can encrypt and decrypt short messages when ", True, self.color_dark)
        self.text2 = self.smallerfont.render("given a key. It is meant to be a learning/ teaching tool to better understand how the Vigenere cipher works,", True, self.color_dark)
        self.text3 = self.smallerfont.render("not a robust encryption/decryption software that can break encryptions.", True, self.color_dark)

        self.sub1 = self.heading.render("How to use this tool", True, self.color_dark)
        self.ins1 = self.smallerfont.render("1. From the Main Menu, click on 'Visualization Tool'", True, self.color_dark)
        self.ins2 = self.smallerfont.render("2. Input the text you want encrypted or decryped in the 'message' box", True, self.color_dark)
        self.ins3 = self.smallerfont.render("3. Input the key you want or need used to either encrypty or decrypt the text in the 'key' box", True, self.color_dark)
        self.ins4 = self.smallerfont.render("4. Click on either 'encrypt' or 'decrypt' to process the text", True, self.color_dark)

        self.sub2 = self.heading.render("Controls", True, self.color_dark)
        self.cont1 = self.controls.render("Playing/ Paused:", True, self.color_dark)
        self.cont2 = self.controls.render("Step Forward/ Step Back:", True, self.color_dark)
        self.cont3 = self.controls.render("Speed Up/ Slow Down:", True, self.color_dark)
        self.cont4 = self.controls.render("Restart:", True, self.color_dark)
        self.cont5 = self.controls.render("Go Back:", True, self.color_dark)

        self.ctxt1 = self.smallerfont.render("This button toggles playing or pausing the animation", True, self.color_dark)
        self.ctxt2 = self.smallerfont.render("When paused these buttons will either go forward or backward one step in the animation", True, self.color_dark)
        self.ctxt3 = self.smallerfont.render("These buttons will either speed up or slow the speed of the animation", True, self.color_dark)
        self.ctxt4 = self.smallerfont.render("This button will restart the animation in a paused state", True, self.color_dark)
        self.ctxt5 = self.smallerfont.render("This button will take you back to the visualization menu to try a new encryption/ decryption", True, self.color_dark)

    def Input(self, events, pressed_keys, mouse):
        for ev in events:
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on a
                # button the game does the thing
                for i in self.buttons:
                    if i.hover(mouse):
                        i.click()

    def Render(self, screen, mouse):
        # fills the screen with a color
        screen.fill((255, 255, 165))
        # buttons and their locations/functions
        menu_button = button(self.height / 1.1, self.menu, lambda: self.SwitchToScene(StartMenu()), self.width / 2 + 350,
                             170, 40)
        other_button = button(self.height / 1.1, self.other, lambda: self.SwitchToScene(About()),
                             self.width / 2 - 500, 270, 40)

        self.buttons = [menu_button, other_button]

        #draw all rendered buttons
        for i in self.buttons:
            i.draw(screen)

        #Title
        screen.blit(self.title, (self.width / 2 - 150, self.height / 30))

        #Information
        screen.blit(self.text1, (self.width / 2 - 625, 120))
        screen.blit(self.text2, (self.width / 2 - 725, 160))
        screen.blit(self.text3, (self.width / 2 - 725, 200))

        screen.blit(self.sub1, (75, 250))
        screen.blit(self.ins1, (150, 290))
        screen.blit(self.ins2, (150, 330))
        screen.blit(self.ins3, (150, 370))
        screen.blit(self.ins4, (150, 410))

        screen.blit(self.sub2, (75, 460))
        screen.blit(self.cont1, (150, 500))
        screen.blit(self.cont2, (150, 540))
        screen.blit(self.cont3, (150, 580))
        screen.blit(self.cont4, (150, 620))
        screen.blit(self.cont5, (150, 660))

        screen.blit(self.ctxt1, (350, 500))
        screen.blit(self.ctxt2, (460, 540))
        screen.blit(self.ctxt3, (420, 580))
        screen.blit(self.ctxt4, (260, 620))
        screen.blit(self.ctxt5, (265, 660))

    def update(self, board, size):
        self.width = size[0]
        self.height = size[1]


class About(SceneManager):
    """
    This menu loads when the user selects the "About ciphers" button in InfoScene()
    This scene informs the user on what ciphers are and how the Vigenere cipher works
    It defines 2 buttons:
        1. Main Menu: this will load the StartMenu() scene, taking the user back to the main menu
        2. Tool information: This will load the Use() scene, flipping the user between the two main info scenes
    """
    def __init__(self):

        SceneManager.__init__(self)
        # white color
        self.color = (255, 255, 255)

        # light shade of the button
        self.color_light = (170, 170, 170)

        # dark shade of the button
        self.color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        self.width = 720

        # stores the height of the
        # screen into a variable
        self.height = 720

        self.x2 = 75

        self.y2 = 30

        # defining a font
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.smallerfont = pygame.font.SysFont('Corbel', 30)
        self.titlefont = pygame.font.SysFont('Corbel', 40, bold = True)
        self.heading = pygame.font.SysFont('Corbel', 35, bold = True)
        self.input_smallfont = pygame.font.SysFont('Corbel', 24)

        # rendering button and title text
        self.menu = self.smallfont.render("Main Menu", True, self.color)
        self.other = self.smallfont.render("Tool Information", True, self.color)
        self.title = self.titlefont.render("Some information on Ciphers", True, self.color_dark)

        #rendering information text
        self.sub1 = self.heading.render("What is a cipher?", True, self.color_dark)
        self.text1 = self.smallerfont.render("A cipher is a system in which plain text is encoded via transposition or subsititution according to", True, self.color_dark)
        self.text2 = self.smallerfont.render("predetermined system. Some betterknown examples are the Caesar cipher, Enigma code, Morse code, ", True, self.color_dark)
        self.text3 = self.smallerfont.render("and even smoke signals. This tool is a visualization of the vigenere cipher.", True, self.color_dark)

        self.sub2 = self.heading.render("The Vigenere Cipher", True, self.color_dark)
        self.txt1 = self.smallerfont.render("First descriped in 1553 it remained unbroken for three centries and gained the title 'le chiffre indechiffrable'", True, self.color_dark)
        self.txt2 = self.smallerfont.render("or 'the indecipherable cipher'. The Vigenere cipher uses two alphabets, one for the text to be altered and", True, self.color_dark)
        self.txt3 = self.smallerfont.render("another for the keyword. These two alphabets form a grid of letters, shifting to the left every row/column.", True, self.color_dark)
        self.txt4 = self.smallerfont.render("The colums are for the text and rows for the keyword. The first letter of each are highlighted and the resulting", True, self.color_dark)
        self.txt5 = self.smallerfont.render("encrypted letter is found in the grid. While for decryption the key letter row is highlighted and the encrypted", True, self.color_dark)
        self.txt6 = self.smallerfont.render("letter will find the plain text column. Keywords are repeated until they reach the lenght necessary to encrypt", True, self.color_dark)
        self.txt7 = self.smallerfont.render("the entire message. For example the keyword 'one' would be 'oneoneoneo' for the plain text 'everything'.", True, self.color_dark)

    def Input(self, events, pressed_keys, mouse):
        for ev in events:
            """
            if ev.type == pygame.QUIT:
                pygame.quit()
            """
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on a
                # button the game does the thing
                for i in self.buttons:
                    if i.hover(mouse):
                        i.click()

    def Render(self, screen, mouse):
        # fills the screen with a color
        screen.fill((255, 255, 165))
        # buttons and their locations/functions
        menu_button = button(self.height / 1.1, self.menu, lambda: self.SwitchToScene(StartMenu()), self.width / 2 + 350,
                             170, 40)
        other_button = button(self.height / 1.1, self.other, lambda: self.SwitchToScene(Use()),
                             self.width / 2 - 500, 240, 40)   

        self.buttons = [menu_button, other_button]

        for i in self.buttons:
            i.draw(screen)

        #Title
        screen.blit(self.title, (self.width / 2 - 200, self.height / 30))

        #Information

        screen.blit(self.sub1, (150, 120))
        screen.blit(self.text1, (self.width / 2 - 600, 170))
        screen.blit(self.text2, (self.width / 2 - 650, 220))
        screen.blit(self.text3, (self.width / 2 - 650, 270))

        screen.blit(self.sub2, (150, 350))
        screen.blit(self.txt1, (self.width / 2 - 600, 400))
        screen.blit(self.txt2, (self.width / 2 - 650, 450))
        screen.blit(self.txt3, (self.width / 2 - 650, 500))
        screen.blit(self.txt4, (self.width / 2 - 650, 550))
        screen.blit(self.txt5, (self.width / 2 - 650, 600))
        screen.blit(self.txt6, (self.width / 2 - 650, 650))
        screen.blit(self.txt7, (self.width / 2 - 650, 700))

    def update(self, board, size):
        self.width = size[0]
        self.height = size[1]
'''