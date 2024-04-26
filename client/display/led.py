import sys
sys.path.append("..")
sys.path.append(".")

import numpy as np
import board
import neopixel
from .map_pixels import PixelMapper # Need to remove the . if running this file on its own
from general_display import Display, to_rgb
import time

ON_DISPLAY = True

def to_rgb(rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        if not ON_DISPLAY:
            return "#%02x%02x%02x" % rgb
        return (rgb[1], rgb[0], rgb[2])

class LEDDisplay(Display):
    """
    Displays pixel data on an LED strip
    """

    def __init__(self, num_strips: int, num_pixels_per_strip: int, start_bottom: bool = True, pixel_pin=board.D18) -> None:
        """
        Initialize the LEDDisplay

        :param num_strips: Number of LED strips
        :param num_pixels_per_strip: Number of pixels per strip
        :param start_bottom: Whether to start from the bottom of the column
        :param pixel_pin: The pin the LED strip is connected to
        """

        self.pixel_mapper = PixelMapper(num_strips, num_pixels_per_strip, start_bottom)

        self.num_pixels = num_strips * num_pixels_per_strip

        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, brightness=0.5, auto_write=False, pixel_order=neopixel.RGB
        )

        self.width = num_strips
        self.height = num_pixels_per_strip

        self.pixels.fill((0, 0, 0))
        self.digits = [[[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
                       [[0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
                       [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
                       [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
                       [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
                       [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
                       [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
                       [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
                       [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
                       [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]]

    def show(self) -> None:
        """
        Show the LED strip
        """
        self.pixels.show()

    def fill_with_digits(x, y):
        pass # TODO

    def display(self, display: np.ndarray) -> None:
        """
        Display the given display on the LED strip

        :param display: The display to show
        """

        # Mirror vertically
        # display = np.flipud(display)

        pixels = self.pixel_mapper.map_pixels(display)

        for i, pixel in enumerate(pixels):
            self.pixels[i] = tuple(pixel.astype(int))

    def clear(self) -> None:
        """
        Clear the LED strip
        """
        self.pixels.fill((0, 0, 0))

    def set_brightness(self, brightness: float) -> None:
        """
        Set the brightness of the LED strip

        :param brightness: The brightness to set
        """
        self.pixels.brightness = brightness

    def set_pixel(self, x: int, y: int, color: tuple) -> None:
        """
        Set the color of a single pixel

        :param index: The index of the pixel
        :param color: The color to set
        """
        
        index = self.pixel_mapper.get_index(x, y)

        if index is None or index >= self.width * self.height:
            return

        self.pixels[index] = color

    def set_pixels(self, colors: list, indices: list) -> None:
        """
        Set the colors of multiple pixels

        :param colors: The colors to set
        """
        for index, color in zip(indices, colors):
            self.pixels[index] = color

    def set_all_pixels(self, color: tuple) -> None:
        """
        Set the color of all pixels

        :param color: The color to set
        """
        self.pixels.fill(color)
    
    def show_digit(self, num, color, x, y):
        for i in range(5):
            for j in range(3):
                if self.digits[num][i][j] == 1:
                    self.set_pixel(j + x, i + y, to_rgb(color))
    
    def pane_digit(self, num, panex, paney, color):
        for i in range(5):
            for j in range(3):
                if self.digits[num][i][j] == 1:
                    self.set_pixel(j + 3*panex, i + 5*paney, to_rgb(color))



if __name__ == "__main__":
    ld = LEDDisplay(27, 20, start_bottom=True)

    # Clear the display
    ld.clear()

    ld.show()

    # display = np.zeros((20, 27, 3))

    # # Red rectangle around the outside
    # display[0, :, :] = [0, 0, 255] # Set top to blue for calibration
    # display[-1, :, :] = [0, 255, 0]
    # display[:, 0, :] = [255, 0, 0] # Set left to green
    # display[:, -1, :] = [0, 255, 0]

    # display[13, :, :] = [0, 0, 255] # Set top to blue for calibration
    # display[:, 10, :] = [0, 0, 255] # Set top to blue for calibration

    # # Green rectangle in the middle
    # display[5:15-3, 5:22-3, :] = [255, 0, 0]

    # # print top row of pixels
    # print(display[0, :, :])

    # # Set 0,0 pixel to white
    # # display[0,0,:] = [255, 255, 255]

    # ld.display(display)

    for x in range(27):
        for y in range(20):

            ld.set_pixel(x, y, (255, 0, 0))

            time.sleep(0.05)

            ld.show()



