import numpy as np


class PixelMapper:
    """
    LED strips will be arranged into a weaved column
    We need to map them to the correct pixel in the 1D strip

    Ex. wiring order

        0  19 20
        1  18 21
        2  17 22
        3  16 23
        4  15 24
        5  14 25
        6  13 26
        7  12 27
        8  11 28
        9  10 29

    Note how the pixels are weaved in the column
    This class provides a method to map the pixels to the correct pixel in the 1D strip
    """

    def __init__(self, num_strips: int, num_pixels_per_strip: int, start_bottom: bool = True) -> None:
        """
        Initialize the PixelMapper

        :param num_strips: Number of LED strips
        :param num_pixels_per_strip: Number of pixels per strip
        :param start_bottom: Whether to start from the bottom of the column
        """

        assert num_strips > 0, "Number of strips must be greater than 0"
        assert num_pixels_per_strip > 0, "Number of pixels per strip must be greater than 0"

        self.num_strips = num_strips
        self.num_pixels_per_strip = num_pixels_per_strip
        self.start_bottom = start_bottom

    def map_pixels(self, display: np.ndarray) -> np.array:
        """
        Maps the display to the correct pixel in the 1D strip

        Ex. display = [
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
        ]

        The display will be mapped to the 1D strip, weaving the pixels in the column

        :param display: The display to map
        :return: The mapped display
        """

        leds = np.zeros((self.num_strips * self.num_pixels_per_strip, 3))

        for i in range(self.num_strips):
            col = display[:, i, :]

            col = np.flip(col, axis=0) if (self.start_bottom and i % 2 == 0) or (not self.start_bottom and i % 2) else col

            leds[i * self.num_pixels_per_strip: (i + 1) * self.num_pixels_per_strip] = col
    
        return leds
    
    def get_index(self, x, y):
        """
        Get the index of the pixel in the 1D strip

        :param x: The x coordinate
        :param y: The y coordinate

        :return: The index of the pixel in the 1D strip

        Ex. get_index(0, 0) = 0
        """

        if self.start_bottom:
            return x * self.num_pixels_per_strip + y
        else:
            return x * self.num_pixels_per_strip + (self.num_pixels_per_strip - y - 1)


if __name__ == "__main__":

    pm = PixelMapper(3, 10, start_bottom=False)

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

    leds = pm.map_pixels(display)

    print(leds)
