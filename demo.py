import time
from PIL import Image
from ws281xMatrix import WS281xMatrix

im = Image.open('sample.png')
pad_size = (max(im.size), max(im.size)) #square
pad = Image.new("RGB", pad_size)
pad.paste(im, (int((pad_size[0]-im.size[0])*0.5),
               int((pad_size[1]-im.size[1])*0.5)))
new_size = (16,16)
im.thumbnail(new_size)
pix = im.load()

frame = []
for i in xrange(new_size[0]):
    row = []
    for j in xrange(new_size[1]):
	row.append(pix[i,j])
    frame.append(row)

screen = WS281xMatrix()

def change_color(color):
    screen.next_frame(screen.blank_frame(color))

try:
    while True:
	screen.next_frame(frame)
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
