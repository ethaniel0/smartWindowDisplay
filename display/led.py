import numpy as np
import board
import neopixel
from map_pixels import PixelMapper


class LEDDisplay:
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
            pixel_pin, self.num_pixels, brightness=0.2, auto_write=True, pixel_order=neopixel.RGB
        )

        self.pixels.fill((0, 0, 0))


    def display(self, display: np.ndarray) -> None:
        """
        Display the given display on the LED strip

        :param display: The display to show
        """
        pixels = self.pixel_mapper.map_pixels(display)

        for i, pixel in enumerate(pixels):
            self.pixels[i] = tuple(pixel)

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

    def set_pixel(self, index: int, color: tuple) -> None:
        """
        Set the color of a single pixel

        :param index: The index of the pixel
        :param color: The color to set
        """
        self.pixels[index] = color

    def set_pixels(self, colors: list) -> None:
        """
        Set the colors of multiple pixels

        :param colors: The colors to set
        """
        for i, color in enumerate(colors):
            self.pixels[i] = color

    def set_all_pixels(self, color: tuple) -> None:
        """
        Set the color of all pixels

        :param color: The color to set
        """
        self.pixels.fill(color)



if __name__ == "__main__":
    ld = LEDDisplay(3, 10, start_bottom=False)

    display = np.array([
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
        [[19, 20, 21], [22, 23, 24], [25, 26, 27]],
        [[28, 29, 30], [31, 32, 33], [34, 35, 36]],
        [[37, 38, 39], [40, 41, 42], [43, 44, 45]],
        [[46, 47, 48], [49, 50, 51], [52, 53, 54]],
        [[55, 56, 57], [58, 59, 60], [61, 62, 63]],
        [[64, 65, 66], [67, 68, 69], [70, 71, 72]],
        [[73, 74, 75], [76, 77, 78], [79, 80, 81]],
        [[82, 83, 84], [85, 86, 87], [88, 89, 90]]
    ])

    ld.display(display)