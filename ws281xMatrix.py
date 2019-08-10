"""WS281X Matrix Renderer Class.

Use Case:
  - If you have a NeoPixel (or similar LED panel from ADAFruit or others) or similar LED
    Matrix and would like to display frames, this will make your life easier. Adafruit
    offers a microcontroller library and complains RPi does not meet their timing
    requirements
Usage:
  - TBD
Contents:
  - Matrix Setup Class.
"""

__author__ = "Nishant Arora"
__version__ = '0.0.1'
__maintainer__ = "Nishant Arora"
__email__ = "me@nishantarora.in"


import rpi_ws281x as ws

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
            brightness = 0.1,      # 1: 100%, 0: 0% everything in between.
            led_channel = 0,     # set to '1' for GPIOs 13, 19, 41, 45 or 53
            led_type = None  # Read the documentation to get your strip type.
    ):
        if width < 1 or height < 1:
            raise Exception('Invalid Dimensions')
        if brightness < 0 or brightness > 1:
            raise Exception('Brightness can only be between 0 and 1')
        else:
            brightness = int(brightness * 255)    # Make this more relevant.
        self.width = width
        self.height = height
        self.pixels = width * height
        self.strip = ws.PixelStrip(self.pixels, led_pin, freq, dma_channel, invert,
                                   brightness, led_channel, led_type)
	self.strip.begin()
        self.next_frame(self.blank_frame((255,255,255)))

    def next_frame(self, frame):
        for i in xrange(len(frame)):
            if i%2 == 1:
                frame[i] = list(reversed(frame[i]))

	p = 0
        for i in frame:
            for j in i:
                self.strip.setPixelColor(p, ws.Color(*j))
                p += 1
        self.strip.show()

    def blank_frame(self, color):
        return [[color] * self.width] * self.height
