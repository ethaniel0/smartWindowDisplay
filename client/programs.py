import abc
from abc import abstractmethod
import random
import socketio
import testdisplay
import time

class App(abc.ABC):
    def __init__(self, name: str, sio: socketio.Client, display: testdisplay.TestDisplay):
        self.name: str = name
        self.sio: socketio.Client = sio
        self.display: testdisplay.TestDisplay = display
    
    @abstractmethod
    def restart():
        pass
    
    @abstractmethod
    def update(input: str):
        pass

    def get_options(self):
        return self.options

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Simon(App):
    def __init__(self, sio: socketio.Client, display: testdisplay.TestDisplay):
        super().__init__("Simon", sio, display)
        self.state = "start"
        self.options = ['Red', 'Blue', 'Green', 'Yellow']
        self.sequence = []
        self.user_sequence = []
        self.sequence_length = 1
        self.sequence_index = 0
        self.user_sequence_index = 0
        
        self.last_time = time.perf_counter()
        self.start_anim_frame = 0

    def restart(self):
        self.state = "start"
        self.sequence = []
        self.user_sequence = []
        self.sequence_length = 1
        self.sequence_index = 0
        self.user_sequence_index = 0

    def update(self, input: str):
        if self.state == "start":
            
            now = time.perf_counter()
            if (now - self.last_time) > 1:
                color = (0, 0, 0) if self.start_anim_frame == 1 else (255, 255, 255)
                for i in range(27):
                    self.display.set_pixel(i, 0, testdisplay.to_rgb(color))
                self.last_time = now
                self.start_anim_frame = 1 - self.start_anim_frame
            
            if input:
                self.sequence = []
                self.user_sequence = []
                self.sequence_length = 1
                self.sequence_index = 0
                self.user_sequence_index = 0
                self.state = "running"
                self.generate_sequence()
                print("Simon says: ", self.sequence)
                
        elif self.state == "running":
            if not input or input not in self.options:
                return
            num_input = ['Red', 'Blue', 'Green', 'Yellow'].index(input)
            
            if self.user_sequence_index == self.sequence_length:
                self.user_sequence_index = 0
                self.sequence_index = 0
                self.sequence_length += 1
                self.generate_sequence()
                print("Simon says: ", self.sequence)
            elif num_input != self.sequence[self.sequence_index]:
                print("You lose!")
                self.state = "start"
            else:
                self.user_sequence_index += 1
                self.sequence_index += 1
            self.sio.emit('simon', {'sequence': self.sequence, 'user_sequence': self.user_sequence, 'sequence_length': self.sequence_length})
        self.display.update_frame()
    
    def generate_sequence(self):
        for i in range(self.sequence_length):
            self.sequence.append(self.options[random.randint(0, 3)])
            
class Snake(App):
    def __init__(self, sio: socketio.Client, display: testdisplay.TestDisplay):
        super().__init__("Snake", sio, display)
        self.state = "start"
        self.options = ['up', 'down', 'left', 'right']
        self.snake = [[0, 0]]
        self.food = [random.randint(0, 9), random.randint(0, 9)]
        self.direction = "right"
        self.score = 0
        self.last_time = time.perf_counter()

    def restart(self):
        self.state = "start"
        self.snake = [[0, 0]]
        self.food = [random.randint(0, 27), random.randint(0, 20)]
        self.direction = "right"
        self.score = 0

    def update(self, input: str):
        if self.state == "start":
            self.snake = [[random.randint(0, 27), random.randint(0, 20)]]
            self.score = 0
            self.display.update_frame()
            self.display.set_pixel(self.food[0], self.food[1], testdisplay.to_rgb((255, 0, 0)))
            self.display.set_pixel(self.snake[0][0], self.snake[0][1], testdisplay.to_rgb((0, 255, 0)))
    
            if input:
                self.state = "running"
                self.direction = input
                print("Snake is moving ", self.direction)

        elif self.state == "running":
            self.move()
            if self.snake[0] == self.food:
                self.score += 1
                self.food = [random.randint(0, 9), random.randint(0, 9)]
                self.snake.append(self.snake[-1])
                self.display.set_pixel(self.food[0], self.food[1], testdisplay.to_rgb((255, 0, 0)))
            elif self.snake[0][0] < 0 or self.snake[0][0] > 27 or self.snake[0][1] < 0 or self.snake[0][1] > 20:
                print("You lose!, Score: ", self.score)
                self.restart()
            elif self.snake[0] in self.snake[1:]:
                print("You lose!, Score: ", self.score)
                self.restart()
            self.display.update_frame()
            if input:
                self.change_direction(input)
                print("Snake is moving ", self.direction)
        self.sio.emit('snake', {'snake': self.snake, 'food': self.food, 'score': self.score})

    def move(self):
        if self.last_time + 1 > time.perf_counter(): # 1 second per move
            return
        new_head = self.snake[0].copy()
        if self.direction == "up":
            new_head[1] -= 1
        elif self.direction == "down":
            new_head[1] += 1
        elif self.direction == "left":
            new_head[0] -= 1
        elif self.direction == "right":
            new_head[0] += 1
        self.snake.insert(0, new_head)
        self.display.set_pixel(new_head[0], new_head[1], testdisplay.to_rgb((0, 255, 0)))
        self.display.set_pixel(self.snake[-1][0], self.snake[-1][1], testdisplay.to_rgb((0, 0, 0)))
        self.snake.pop()
        self.last_time = time.perf_counter()

    def change_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"
