"""WS281X Matrix Renderer Class.

Use Case:
  - If you have a NeoPixel (or similar LED panel from ADAFruit or others) or
    similar LED Matrix and would like to display frames, this will make your
    life easier. Adafruit offers a microcontroller library and complains RPi
    does not meet their timing requirements
Usage:
  - TBD
Contents:
  - Matrix Setup Class.
"""

__author__ = "Nishant Arora"
__version__ = '0.0.1'
__maintainer__ = "Nishant Arora"
__email__ = "me@nishantarora.in"

from PIL import Image, ImageSequence
from Queue import Queue
import rpi_ws281x as ws
from threading import Timer

class WS281xMatrix(object):
    """Represents the LED Matrix."""

    def __init__(
            self,
            width = 16,          # Number of pixels in width
            height = 16,         # Number of pixels in height
            led_pin = 18,        # PWM pin
            freq = 800000,       # 800khz
            dma_channel = 10,
            invert = False,      # Invert Shifter, should not be needed
            brightness = 0.1,    # 1: 100%, 0: 0% everything in between.
            led_channel = 0,     # set to '1' for GPIOs 13, 19, 41, 45 or 53
            led_type = None,     # Read the documentation to get your strip type.
            fps = 10             # frames per second.
    ):
        if width < 1 or height < 1:
            raise Exception('Invalid Dimensions')
        if brightness < 0 or brightness > 1:
            raise Exception('Brightness can only be between 0 and 1')
        else:
            brightness = int(brightness * 255)    # Make this more relevant.
        self.width = width
        self.height = height
        self.fps = fps
        self.wh_ratio = width * 1.0 / height
        self.pixels = width * height
        self.strip = ws.PixelStrip(self.pixels, led_pin, freq, dma_channel, invert,
                                   brightness, led_channel, led_type)
        self.strip.begin()
        self.power = True
        self.buffer = Queue()
        self.reset()
        self.loop()

    def kill(self):
        self.power = False
        self.reset()

    def reset(self):
        self.buffer = Queue()
        self.render(self.blank_frame((0,0,0)))

    def loop(self):
	if self.power:
            if not self.buffer.empty():
                frame = self.buffer.get()
                self.render(frame)
            Timer(float(1)/self.fps, self.loop).start()
        else:
            self.reset()

    def next_frame(self, frame, override = False):
	self.queue = Queue()
        for i in xrange(len(frame)):
            if i%2 == 1:
                frame[i] = list(reversed(frame[i]))
        self.buffer.put(frame)

    def render(self, frame):
        p = 0
        for i in frame:
            for j in i:
                self.strip.setPixelColor(p, ws.Color(*j))
                p += 1
        self.strip.show()

    def blank_frame(self, color):
        return [[color] * self.width] * self.height

    def __pad_size(self, size):
        (w,h) = size
        if float(w)/h != self.wh_ratio:
            if max(size) == w:
                return (w, int(w/self.wh_ratio))
            return (int(h*self.wh_ratio), h)
        return size

    def __rgb_translate(self, im):
        pad_size = self.__pad_size(im.size)
        pad = Image.new("RGB", pad_size, (0, 0, 0, 0))
        pad.paste(im, (int((pad_size[0]-im.size[0])*0.5),
                       int((pad_size[1]-im.size[1])*0.5)))
        new_size = (self.width, self.height)
        pad.thumbnail(new_size)

        pix = pad.load()

        frame = []
        for i in xrange(new_size[0]):
            row = []
            for j in xrange(new_size[1]):
                row.append(pix[i,j])
            frame.append(row)
        return frame

    def render_image(self, image_path):
        im = Image.open(image_path)
        frame = self.__rgb_translate(im)
        self.next_frame(frame)

    def render_animation(self, ani_path, loops = 5):
        im = Image.open(ani_path)
        if not im.is_animated:
            raise Exception("Not an animation")
        ani = []

        # translate animation.
        for frame in ImageSequence.Iterator(im):
            ani.append(self.__rgb_translate(frame))

        # Queue the frames
        for loop in xrange(loops):
            for frame in ani:
                self.next_frame(frame)

