import sys
sys.path.append("..")
sys.path.append(".")

import numpy as np
import board
import neopixel
from .map_pixels import PixelMapper # Need to remove the . if running this file on its own
from general_display import Display


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
            pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.RGB
        )

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
        pixels = self.pixel_mapper.map_pixels(display)

        for i, pixel in enumerate(pixels):
            print(tuple(pixel))
            self.pixels[i] = tuple(pixel.astype(int))

        print(type(self.pixels))

        self.pixels.show()

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
    
        c = to_rgb(color)
        for i in range(27 * 20):
            self.pixels[i] = c
    
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

    display = np.zeros((20, 27, 3))

    # Red rectangle around the outside
    display[0, :, :] = [0, 0, 255] # Set top to blue for calibration
    display[-1, :, :] = [0, 255, 0]
    display[:, 0, :] = [255, 0, 0] # Set left to green
    display[:, -1, :] = [0, 255, 0]

    # Green rectangle in the middle
    display[5:15, 5:22, :] = [255, 0, 0]

    # Set 0,0 pixel to white
    display[0,0,:] = [255, 255, 255]

    ld.display(display)
