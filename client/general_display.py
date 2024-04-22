import abc
from abc import abstractmethod

ON_DISPLAY = True

def to_rgb(rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        if not ON_DISPLAY:
            return "#%02x%02x%02x" % rgb
        return (rgb[1], rgb[0], rgb[2])

class Display(abc.ABC):
    def __init__(self):
        ...
        
    @abstractmethod
    def set_pixel(self, x, y, color):
        ...
    
    @abstractmethod
    def set_pixels(self, colors):
        ...
    
    @abstractmethod
    def set_all_pixels(self, color):
        ...

    @abstractmethod
    def show_digit(self, num, color, x, y):
        ...
    
    @abstractmethod
    def pane_digit(self, num, panex, paney, color):
        ...
    
    @abstractmethod
    def fill_with_digits(self, color):
        ...
    
    @abstractmethod
    def clear(self):
        ...
    
    @abstractmethod
    def display(self):
        ...
