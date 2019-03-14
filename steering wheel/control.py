# Imports
import pygame
print("Pygame version: ", pygame.__version__)


class Steering():
    """docstring for Steering"""
    def __init__(self):
        # initialize the pygame
        pygame.init()
        # initialize all the joysticks
        pygame.joystick.init()
        # used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        # get the joystick and initialize it
        self.joystick = self.initialize_joystick()
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
        while True:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    print("Terminating program")
                    self.terminate()
                    exit(0)
                if(event.type == pygame.JOYAXISMOTION):
                    if(event.axis == 0):
                        # Steering wheel motion detected
                        print("angle", ((event.value * 45) + 90))
                    elif(event.axis == 2):
                        # Peddle motion detected (left = 1, right = -1)
                        if(event.value > 0):
                            print("gas has been pressed:", event.value * 99)
                            # Send increase speed and go forward
                        elif(event.value < 0):
                            print("break has been pressed", event.value)
                        else:
                            print("stop the vehicle")
            self.clock.tick(20)

    def terminate(self):
        # uninitialize this joystick
        self.joystick.quit()
        # uninitialize all the joysticks
        pygame.joystick.quit()
        # uninitialize pygame
        pygame.quit()

    def initialize_joystick():
        """Looks to see if a joystick has been plugged in and initializes it"""
        joystick_count = pygame.joystick.get_count()
        if(joystick_count >= 1):
            wheel = pygame.joystick.Joystick(0)
            print("Initialized", wheel.get_id(), "named ", wheel.get_name())
            return wheel.init()
        else:
            print("No joysticks found.")
            exit(-1)


if __name__ == '__main__':
    wheel = Steering()
    wheel.drive()
