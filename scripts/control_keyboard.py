# Imports
import sys
if sys.version_info.major < 3 or sys.version_info.minor < 4:
    raise RuntimeError('At least Python 3.4 is required')

import keyboard
import pygame
import requests

HOST = '10.148.131.75'
PORT = '8000'

# BASE_URL is variant use to save the format of host and port
BASE_URL = 'http://' + HOST + ':'+ PORT + '/'

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
        self.clock = pygame.time.Clock()

        self.backward = False # start with moving forward
        self.direction = 0 # 0 is straight, 1 is left, 2 is right
        self.speed = 60 # initial speed, speed is 0-100
        self.camera_up_angle = 0
        self.camera_left_angle = 0

    def drive(self):
        while True:
            # terminate program press 'q'
            if keyboard.is_pressed('q'):
                print('Terminating program')
                break
            # turn left
            if keyboard.is_pressed('a'):
                if self.direction != 1:
                    self.direction = 1
                    print('left')
                    run_action('fwleft')
            # turn right
            elif keyboard.is_pressed('d'):
                if self.direction != 2:
                    self.direction = 2
                    print('right')
                    run_action('fwright')
            # go straight
            else:
                if self.direction != 0:
                    self.direction = 0
                    print('straight')
                    run_action('fwstraight')
            # move
            if keyboard.is_pressed('w'):
                if not self.backward:
                    print('forward')
                    run_action('forward')
                else:
                    print('backward')
                    run_action('backward')
            # stop
            elif keyboard.is_pressed('s'):
                print('stop')
                run_action('stop')
            # shift gear between forward and backward
            if keyboard.is_pressed('b'):
                if self.backward:
                    print('change mode from backward to forward')
                else:
                    print('change mode from forward to backward')
                self.backward = not self.backward
            # use "i j k l" to control camera direction
            if keyboard.is_pressed('i'):
                if self.camera_up_angle < 60:
                    self.camera_up_angle += 20
                    run_action('camup')
            elif keyboard.is_pressed('k'):
                if self.camera_up_angle > -40:
                    self.camera_up_angle -= 20
                    run_action('camdown')
            elif keyboard.is_pressed('j'):
                if self.camera_left_angle < 3:
                    self.camera_left_angle += 1
                    run_action('camleft')
            elif keyboard.is_pressed('l'):
                if self.camera_left_angle > -3:
                    self.camera_left_angle -= 1
                    run_action('camright')
            # accelerate
            if keyboard.is_pressed('n'):
                if self.speed < 100:
                    self.speed += 20
                    run_speed(str(self.speed))
            # deaccelerate
            elif keyboard.is_pressed('m'):
                if self.speed > 20:
                    self.speed -= 20
                    run_speed(str(self.speed))
            # check keyboard input 10 times every second
            self.clock.tick(10)

if __name__ == '__main__':
    # check connection
    print('connection:', connection_ok())
    wheel = Steering()
    wheel.drive()
