# WS281X NeoPixel-ish Matrix Rendering Library

This library is intended to make the neopixel ish LED matrix to work with raspberry pi and Python. It is based on this [rpi-ws281x](https://github.com/rpi-ws281x/rpi-ws281x-python) python implementation. This makes it setting up your LED panel faster and removes a lot of hiccups. The original library does not work with panel, it is meant to control the strip.

## Features offered

* Direct resizing and rendering of images (png/jpeg).
* Direct resizing and rendering of animations (gif)
* Frames are represented as RGB Tuples so building your own frame is very simple.
* Excellent brightness control.
* Support for multi panel configurations.
* Non-blocking threads, the operations are async and will not block you.

## Setup

You'll need to install pillow and rpi-ws281x packages (and their dependencies from pip)
```
# pip install pillow rpi-ws281x
```

## Demo

```
# python demo.py
```

The order is red -> green -> blue -> image -> animation. If this is not the order you see, your strip config is different than the mine.

## Adding to your project

Add it as a submodule.

```
$ git submodule add https://github.com/whizzzkid/rpi-ws281x-matrix-python matrix
```
In your project
```
from matrix.ws281xMatrix import WS281xMatrix

screen = WS281xMatrix()
```

## API

Once you have:
```
screen = WS281xMatrix()
```

You can simply ask it to render an image like so:
```
screen.render_image('path_to_image')
```

## Why is this needed?
When I wrote this, I was frustrated to make [this 16x16 panel](https://amzn.to/2H10an3) work with RPi. The Adafruit Neopixel library claims that their panels cannot work with RPi because of their strict timing requirements. However that is not the case. The rpi-281x library is a proof that it works, however it does not allow you to dump images/animations directly on the screen. This library aims to solve just that.

## License
MIT
