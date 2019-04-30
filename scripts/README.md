These are two programs that can control the remote driving car. "control_keyboard.py" uses keyboard to control and "control_steering_wheel.py" uses steering wheel. The server program "./server/remote_control/start" needs to be running on the remote driving car's raspberry pi. The server program is customized based on https://github.com/sunfounder/SunFounder_PiCar-V.

keyboard control:
q: terminate program

w: move forward
s: stop
a: turn left
d: turn right

b: shift mode between moving forward and backward

i: camera move up
k: camera move down
j: camera move left
l: camera move right

n: increase speed level by 20
m: decrease speed level by 20

#############################

steering wheel control:
ctrl c: terminate program

steer left: turn left
steer right: turn right

gas pedal: increase speed
break pedal: stop

button 9: shift mode between moving forward and backward
button 4: camera move left
button 5: camera move right