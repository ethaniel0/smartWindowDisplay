import tkinter as tk
import random

def to_rgb(rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb

class TestDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Display")
        self.geometry("270x200")
        self.canvas = tk.Canvas(self, width=270, height=200)
        for i in range(27):
            for j in range(20):
                self.set_pixel(i, j, to_rgb((0, 0, 0)))
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
    
    def set_pixel(self, x, y, color):
        self.canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill=color, outline="")
        self.canvas.pack()
    
    def set_pixels(self, colors):
        for i, color in enumerate(colors):
            x = i % 27
            y = i // 27
            self.set_pixel(x, y, to_rgb(color))
    
    def set_all_pixels(self, color):
        self.canvas.create_rectangle(0, 0, 270, 200, fill=to_rgb(color))
    
    def pane_digit(self, num, panex, paney, color):
        print("Displaying number: ", num, " in pane ", panex, paney)
        for i in range(5):
            for j in range(3):
                if self.digits[num][i][j] == 1:
                    self.set_pixel(j + 3*panex, i + 5*paney, to_rgb(color))
    
    def fill_with_digits(self, color):
        for i in range(9):
            for j in range(4):
                num = random.randint(0, 9)
                self.pane_digit(num, i, j, color)
    
    def clear(self):
        self.set_all_pixels((0, 0, 0))
    
    def update_frame(self):
        self.update_idletasks()
        self.update()

if __name__ == "__main__":
    display = TestDisplay()
    display.set_all_pixels((255, 0, 0))
    display.update_frame()
    display.set_all_pixels((0, 255, 0))
    display.update_frame()
    display.set_all_pixels((0, 0, 255))
    display.update_frame()
    display.set_all_pixels((0, 0, 0))
    display.update_frame()
    display.set_pixel(0, 0, to_rgb((255, 255, 255)))
    display.mainloop()