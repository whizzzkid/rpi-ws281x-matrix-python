import time
from ws281x-matrix import WS281xMatrix

screen = WS281xMatrix()

try:
    while True:
        print('Red')
        screen.next_frame(blank_frame((255,0,0)))
        time.sleep(1)
        print('Green')
        screen.next_frame(blank_frame((0,255,0)))
        time.sleep(1)
        print('Blue')
        screen.next_frame(blank_frame((0,0,255)))
        time.sleep(1)
except KeyboardInterrupt:
    screen.next_frame(blank_frame(0,0,0))
