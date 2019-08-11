import os
import time
from ws281xMatrix import WS281xMatrix

im = os.path.join(path, 'sample.png')
ani = os.path.join(path, 'sample.gif')

screen = WS281xMatrix()

def change_color(color):
    screen.next_frame(screen.blank_frame(color))

try:
    while True:
	    screen.render_image(im)
	    time.sleep(50)
        screen.render_animation(ani)
        time.sleep(50)
        print('Red')
        change_color((255,0,0))
        time.sleep(2)
        print('Green')
        change_color((0,255,0))
        time.sleep(2)
        print('Blue')
        change_color((0,0,255))
        time.sleep(2)
except KeyboardInterrupt:
    change_color((0,0,0))
