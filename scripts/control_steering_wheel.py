# Imports
import sys
if sys.version_info.major < 3 or sys.version_info.minor < 4:
    raise RuntimeError('At least Python 3.4 is required')

import pygame
print("Pygame version: ", pygame.__version__)

import requests

HOST      = '10.148.131.75'
PORT      = '8000'

# BASE_URL is variant use to save the format of host and port
BASE_URL = 'http://' + HOST + ':'+ PORT + '/'

            # elif key_press == Qt.Key_W:         # W
            #     run_action('forward')
            # elif key_press == Qt.Key_A:         # A
            #     run_action('fwleft')
            # elif key_press == Qt.Key_S:         # S
            #     run_action('backward')
            # elif key_press == Qt.Key_D:         # D
            #     run_action('fwright')

def __request__(url, times=10):
    for x in range(times):
        try:
            requests.get(url)
            return 0
        except :
            print("Connection error, try again")
    print("Abort")
    return -1


def run_action(cmd):
    """Ask server to do sth, use in running mode

    Post requests to server, server will do what client want to do according to the url.
    This function for running mode

    Args:
        # ============== Back wheels =============
        'bwready' | 'forward' | 'backward' | 'stop'

        # ============== Front wheels =============
        'fwready' | 'fwleft' | 'fwright' |  'fwstraight'

        # ================ Camera =================
        'camready' | 'camleft' | 'camright' | 'camup' | 'camdown'
    """
    # set the url include action information
    url = BASE_URL + 'run/?action=' + cmd
    print('url: %s'% url)
    # post request with url 
    __request__(url)

def run_speed(speed):
    """Ask server to set speed, use in running mode

    Post requests to server, server will set speed according to the url.
    This function for running mode.

    Args:
        '0'~'100'
    """
    # Set set-speed url
    url = BASE_URL + 'run/?speed=' + speed
    print('url: %s'% url)
    # Set speed
    __request__(url)

def connection_ok():
    """Check whetcher connection is ok

    Post a request to server, if connection ok, server will return http response 'ok' 

    Args:
        none

    Returns:
        if connection ok, return True
        if connection not ok, return False
    
    Raises:
        none
    """
    cmd = 'connection_test'
    url = BASE_URL + cmd
    print('url: %s'% url)
    # if server find there is 'connection_test' in request url, server will response 'Ok'
    try:
        r=requests.get(url)
        if r.text == 'OK':
            return True
    except:
        return False


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
        self.joystick.init()
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
        self.backward = False
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
                        angle = (event.value * 45) + 90
                        print("angle", angle)
                        if angle <= 85:
                            run_action('fwleft')
                        elif angle >= 95:
                            run_action('fwright')
                        else:
                            run_action('fwstraight')

                    elif(event.axis == 2):
                        # Peddle motion detected (left = 1, right = -1)
                        if(event.value > 0):
                            speed = event.value * 99
                            print("gas has been pressed:", speed)
                            run_speed(str(int(speed)))
                            if not self.backward:
                                run_action('forward')
                            else:
                                run_action('backward')
                            # Send increase speed and go forward
                        elif(event.value < 0):
                            print("break has been pressed", event.value)
                            run_action('stop')
                        # else:
                        #     print("stop the vehicle")
                if event.type == pygame.JOYBUTTONDOWN:
                    # print(event)
                    if event.button == 9:
                        self.backward = not self.backward
                        print('backward state:', self.backward)
                    elif event.button == 4:
                        run_action('camleft')
                    elif event.button == 5:
                        run_action('camright')
            self.clock.tick(20)

    def terminate(self):
        # uninitialize this joystick
        self.joystick.quit()
        # uninitialize all the joysticks
        pygame.joystick.quit()
        # uninitialize pygame
        pygame.quit()

    def initialize_joystick(self):
        """Looks to see if a joystick has been plugged in and initializes it"""
        joystick_count = pygame.joystick.get_count()
        if(joystick_count >= 1):
            wheel = pygame.joystick.Joystick(0)
            print("Initialized", wheel.get_id(), "named ", wheel.get_name())
            return wheel
        else:
            print("No joysticks found.")
            exit(-1)


if __name__ == '__main__':
    wheel = Steering()
    wheel.drive()
    # print(connection_ok())
