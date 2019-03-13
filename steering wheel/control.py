import pygame

class Steering():
    """docstring for Steering"""
    def __init__(self):
        # initialize the pygame
        pygame.init()
        # initialize all the joysticks
        pygame.joystick.init()
        # used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        # check if there is only one joystick
        assert pygame.joystick.get_count() >= 1, "Didn\'t get one joystick."
        assert pygame.joystick.get_count() <= 1, "Get multiple joysticks."
        # get the joystick and initialize it
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print('Joystick', self.joystick.get_name(), 'with id', self.joystick.get_id(), 'has been initialized.')
        # get the number of axes
        self.axes = self.joystick.get_numaxes()
        print(self.axes, "axes get.")
        # get the number of balls
        self.balls = self.joystick.get_numballs()
        print(self.balls, "balls get.")
        # get the number of buttons
        self.buttons = self.joystick.get_numbuttons()
        print(self.buttons, "buttons get.")
        # get the number of hats
        self.hats = self.joystick.get_numhats()
        print(self.hats, "hats get.")
        """ event attributes and event type
        QUIT             none
        ACTIVEEVENT      gain, state
        KEYDOWN          unicode, key, mod
        KEYUP            key, mod
        MOUSEMOTION      pos, rel, buttons
        MOUSEBUTTONUP    pos, button
        MOUSEBUTTONDOWN  pos, button
        JOYAXISMOTION    joy, axis, value
        JOYBALLMOTION    joy, ball, rel
        JOYHATMOTION     joy, hat, value
        JOYBUTTONUP      joy, button
        JOYBUTTONDOWN    joy, button
        VIDEORESIZE      size, w, h
        VIDEOEXPOSE      none
        USEREVENT        code
        """
        # block everything except quit, activeevent, joyaxismotion, userevent
        # pygame.event.set_blocked(pygame.KEYDOWN)
        # pygame.event.set_blocked(pygame.KEYUP)
        # pygame.event.set_blocked(pygame.MOUSEMOTION)
        # pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        # pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        # pygame.event.set_blocked(pygame.JOYBALLMOTION)
        # pygame.event.set_blocked(pygame.JOYHATMOTION)
        # pygame.event.set_blocked(pygame.JOYBUTTONUP)
        # pygame.event.set_blocked(pygame.JOYBUTTONDOWN)
        # pygame.event.set_blocked(pygame.VIDEORESIZE)
        # pygame.event.set_blocked(pygame.VIDEOEXPOSE)

        # self.left = None
        # self.right = None

    def drive(self):
        loop = True
        while loop:
            # process event
            for event in pygame.event.get():
                print(event, 'detected.')
                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                # if event.type == pygame.JOYAXISMOTION:
                #     print("----------------axes---------------")
                #     for i in range(self.axes):
                #         print(i, self.joystick.get_axis(i))
                if event.type == pygame.QUIT:
                    loop = False
            # limit to 20 frames per second
            self.clock.tick(20)
        self.terminate()

    def terminate(self):
        # uninitialize this joystick
        self.joystick.quit()
        # uninitialize all the joysticks
        pygame.joystick.quit()
        # uninitialize pygame
        pygame.quit()

        

if __name__ == '__main__':
    wheel = Steering()
    wheel.drive()