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
        self.sequence_index = 0
        self.user_sequence_index = 0
        
        self.last_time = time.perf_counter()
        self.start_anim_frame = 0
        
        self.started_show_sequence = False

    def restart(self):
        self.state = "start"
        self.sequence = []
        self.user_sequence = []
        self.sequence_index = 0
        self.user_sequence_index = 0
        
    def start_state(self, input: str):
        if input:
            self.sequence = []
            self.user_sequence = []
            self.sequence_index = 0
            self.user_sequence_index = 0
            self.state = "showing"
            self.add_to_sequence()
            print("Simon says: ", self.sequence)
            self.display.clear()
            return
        
        now = time.perf_counter()
        if (now - self.last_time) > 1:
            color = (0, 0, 0) if self.start_anim_frame == 1 else (255, 255, 255)
            for i in range(27):
                self.display.set_pixel(i, 0, testdisplay.to_rgb(color))
            self.last_time = now
            self.start_anim_frame = 1 - self.start_anim_frame
            
    def show_rect(self, x, y, w, h, color):
        for i in range(x, x + w):
            for j in range(y, y + h):
                self.display.set_pixel(i, j, testdisplay.to_rgb(color))
        
    def show_sequence(self):
        if not self.started_show_sequence:
            self.last_time = time.perf_counter()
            self.started_show_sequence = True
        now = time.perf_counter()
        if now - self.last_time > 1:
            self.last_time = now
            self.sequence_index += 1
            
        if self.sequence_index >= len(self.sequence):
            self.state = "running"
            self.sequence_index = 0
            self.user_sequence_index = 0
            self.started_show_sequence = False
            self.display.clear()
            return
        
        color_map = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
        seq_num = self.sequence[self.sequence_index]
        color = color_map[seq_num]
        
        self.show_rect(5, 5, 5, 5, (80, 0, 0))
        self.show_rect(10, 5, 5, 5, (0, 0, 80))
        self.show_rect(5, 10, 5, 5, (0, 80, 0))
        self.show_rect(10, 10, 5, 5, (80, 80, 0))
        
        if now - self.last_time < 0.8:
            if seq_num == 0:
                self.show_rect(5, 5, 5, 5, color)
            elif seq_num == 1:
                self.show_rect(10, 5, 5, 5, color)
            elif seq_num == 2:
                self.show_rect(5, 10, 5, 5, color)
            elif seq_num == 3:
                self.show_rect(10, 10, 5, 5, color)
        
        now = time.perf_counter()

    def get_input(self, input: str):
        if not input or input not in self.options:
            return
        
        num_input = ['Red', 'Blue', 'Green', 'Yellow'].index(input)
        
        print("User input: ", num_input)
        
        if num_input != self.sequence[self.sequence_index]:
            print("You lose!")
            self.state = "start"
            return
        else:
            print('Correct!')
            self.sequence_index += 1
            self.user_sequence_index += 1
        
        print('going onto next')
            
        if self.user_sequence_index == len(self.sequence):
            print("You win!")
            self.sequence_index = 0
            self.user_sequence_index = 0
            self.add_to_sequence()
            self.state = "showing"
            print("Simon says: ", self.sequence)

    def update(self, input: str):
        if self.state == "start":
            self.start_state(input)
        elif self.state == "showing":
            self.show_sequence()
        elif self.state == "running":
            self.get_input(input)
        self.display.update_frame()

    def add_to_sequence(self):
        self.sequence.append(random.randint(0, 3))
              
class Snake(App):
    def __init__(self, sio: socketio.Client, display: testdisplay.TestDisplay):
        super().__init__("Snake", sio, display)
        self.state = "start"
        self.options = ['up', 'down', 'left', 'right']
        self.snake = [[0, 0]]
        self.food = [0,0]
        self.direction = "right"
        self.score = 0
        self.eaten = False
        self.last_time = time.perf_counter()

    def restart(self):
        self.state = "start"
        self.snake = [[random.randint(0, 26), random.randint(0, 19)]]
        self.food = [random.randint(0, 26), random.randint(0, 19)]
        self.display.clear()
        self.direction = "right"
        self.score = 0

    def update(self, input: str):
        if self.state == "start":
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
                self.food = [random.randint(0, 26), random.randint(0, 19)]
                self.eaten = True
            elif self.snake[0][0] < 0 or self.snake[0][0] > 26 or self.snake[0][1] < 0 or self.snake[0][1] > 19:
                print("You lose!, Score: ", self.score)
                self.restart()
            elif self.snake[0] in self.snake[1:]:
                print("You lose!, Score: ", self.score)
                self.restart()
            self.display.update_frame()
            self.display.set_pixel(self.food[0], self.food[1], testdisplay.to_rgb((255, 0, 0)))
            if input:
                self.change_direction(input)
                print("Snake is moving ", self.direction)

    def move(self):
        if self.last_time + 0.25 > time.perf_counter(): # 1 second per move
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
        if not self.eaten:
            self.display.set_pixel(self.snake[-1][0], self.snake[-1][1], testdisplay.to_rgb((0, 0, 0)))
            self.snake.pop()
        else:
            self.eaten = False
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

class Maze(App):
    def __init__(self, sio: socketio.Client, display: testdisplay.TestDisplay):
        super().__init__("Maze", sio, display)
        self.state = "start"
        self.options = ['up', 'down', 'left', 'right']
        self.player = [0, 0]
        self.goal = [26, 19]
        self.last_time = time.perf_counter()
        self.maze = [[0 for i in range(27)] for j in range(20)]

    def generate_maze(self):
        #randomly generate a maze
        for i in range(27):
            for j in range(20):
                if random.random() < 0.3:
                    self.maze[j][i] = 1
    
    def display_maze(self):
        for i in range(27):
            for j in range(20):
                if self.maze[j][i] == 1:
                    self.display.set_pixel(i, j, testdisplay.to_rgb((0, 0, 0)))
                else:
                    self.display.set_pixel(i, j, testdisplay.to_rgb((255, 255, 255)))

    def restart(self):
        self.state = "start"
        self.player = [0, 0]
        self.goal = [26, 19]
        # self.display.clear()
        # self.generate_maze()
        # self.display_maze()

    def update(self, input: str):
        if self.state == "start":
            self.display.update_frame()
            self.display.set_pixel(self.goal[0], self.goal[1], testdisplay.to_rgb((255, 0, 0)))
            self.display.set_pixel(self.player[0], self.player[1], testdisplay.to_rgb((0, 255, 0)))
            if input:
                self.state = "running"
                self.direction = input
                print("Maze is moving ", self.direction)

        elif self.state == "running":
            if input:
                self.change_direction(input)
                print("Maze is moving ", self.direction)
                self.move()
                self.display.update_frame()
            if self.player == self.goal:
                print("You win!")
                self.restart()

    def move(self):
        if self.direction == "up":
            self.player[1] -= 1
        elif self.direction == "down":
            self.player[1] += 1
        elif self.direction == "left":
            self.player[0] -= 1
        elif self.direction == "right":
            self.player[0] += 1
        print ("player now at: ", self.player)
        self.display.set_pixel(self.player[0], self.player[1], testdisplay.to_rgb((0, 255, 0)))
        
    def change_direction(self, direction):
        if direction == "up":
            self.direction = "up"
        elif direction == "down":
            self.direction = "down"
        elif direction == "left":
            self.direction = "left"
        elif direction == "right":
            self.direction = "right"

class Jump(App):
    def __init__(self, sio: socketio.Client, display: testdisplay.TestDisplay):
        super().__init__("Jump", sio, display)
        self.state = "start"
        self.options = ['up', 'down']
        self.player = [0, 0]
        self.course = [[0 for i in range(27)] for j in range(20)]
        self.set_course()
        self.last_time = time.perf_counter()
        self.obstacles = []

    def set_course(self):
        for i in range(27):
            for j in range(20):
                if j < 10:
                    self.course[j][i] = 0
                else:
                    self.course[j][i] = 1

    def generate_obstacles(self):
        #randomly generate obstacles
        if random.random() < 0.3:
            if random.random() < 0.5:
                self.obstacles.append([26, 10]) #low obstacle
            else:
                self.obstacles.append([26, 8]) #high obstacle 
        
    def move(self):
        if self.direction == "up":
            self.player[1] -= 1
        elif self.direction == "down":
            self.player[1] += 1  