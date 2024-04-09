import abc
from abc import abstractmethod
import random
import socketio

class App(abc.ABC):
    def __init__(self, name: str, sio: socketio.Client):
        self.name: str = name
        self.sio: socketio.Client = sio
    
    @abstractmethod
    def restart():
        pass
    
    @abstractmethod
    def update():
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Simon(App):
    def __init__(self, sio: socketio.Client):
        super().__init__("Simon", sio)
        self.state = "start"
        self.options = ['Red', 'Blue', 'Green', 'Yellow']
        self.sequence = []
        self.user_sequence = []
        self.sequence_length = 1
        self.sequence_index = 0
        self.user_sequence_index = 0

    def restart(self):
        self.state = "start"
        self.sequence = []
        self.user_sequence = []
        self.sequence_length = 1
        self.sequence_index = 0
        self.user_sequence_index = 0

    def update(self):
        if self.state == "start":
            self.sequence = []
            self.user_sequence = []
            self.sequence_length = 1
            self.sequence_index = 0
            self.user_sequence_index = 0
            self.state = "running"
            self.generate_sequence()
            print("Simon says: ", self.sequence)
        elif self.state == "running":
            if self.user_sequence_index == self.sequence_length:
                self.user_sequence_index = 0
                self.sequence_index = 0
                self.sequence_length += 1
                self.generate_sequence()
                print("Simon says: ", self.sequence)
            elif self.user_sequence[self.user_sequence_index] != self.sequence[self.sequence_index]:
                print("You lose!")
                self.state = "start"
            else:
                self.user_sequence_index += 1
                self.sequence_index += 1
        self.sio.emit('simon', {'sequence': self.sequence, 'user_sequence': self.user_sequence, 'sequence_length': self.sequence_length})

    def generate_sequence(self):
        for i in range(self.sequence_length):
            self.sequence.append(self.options[random.randint(0, 3)])
            
class Snake(App):
    def __init__(self, sio: socketio.Client):
        super().__init__("Snake", sio)
        self.state = "start"
        self.snake = [[0, 0]]
        self.food = [random.randint(0, 9), random.randint(0, 9)]
        self.direction = "right"
        self.score = 0

    def restart(self):
        self.state = "start"
        self.snake = [[0, 0]]
        self.food = [random.randint(0, 9), random.randint(0, 9)]
        self.direction = "right"
        self.score = 0

    def update(self):
        if self.state == "start":
            self.state = "running"
        elif self.state == "running":
            self.move()
            if self.snake[0] == self.food:
                self.score += 1
                self.food = [random.randint(0, 9), random.randint(0, 9)]
            elif self.snake[0][0] < 0 or self.snake[0][0] > 9 or self.snake[0][1] < 0 or self.snake[0][1] > 9:
                print("You lose!")
                self.state = "start"
            elif self.snake[0] in self.snake[1:]:
                print("You lose!")
                self.state = "start"
        self.sio.emit('snake', {'snake': self.snake, 'food': self.food, 'score': self.score})

    def move(self):
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
        self.snake.pop()

    def change_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"
