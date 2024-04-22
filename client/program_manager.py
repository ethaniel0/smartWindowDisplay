import socketio
import programs
import testdisplay
from threading import Semaphore

class ProgramManager:
    def __init__(self, sio: socketio.Client, display: testdisplay.TestDisplay):
        self.state = "main"
        self.sio = sio
        self.display = display

        self.pages = {
            "main": ["Duke Game", "Weather", "Games"],
            "Games": ["Simon", "Snake", "Maze", "Jump", "BadApple"],
            "Duke Game": "Duke Game", 
    
            "Simon": programs.Simon(sio, self.display),
            "Snake": programs.Snake(sio, self.display),
            "Maze": programs.Maze(sio, self.display),
            "Jump": programs.Jump(sio, self.display),
            "BadApple": programs.BadApple(sio, self.display),
        }
        
        self.last_input = ""
        self.startup = False
        
    
    def go_one_page_up(self):
        print("going one page up")
        if self.state == "main":
            self.state = "main"
        
        found = False
        
        for key in self.pages:
            if not isinstance(self.pages[key], list):
                continue
            
            for item in self.pages[key]:
                if item == self.state:
                    self.state = key
                    found = True
                    break
            if found:
                break  
        
        name_list = []
        for name in self.pages[self.state]:
            if isinstance(name, str):
                name_list.append(name)
            else:
                name_list.append(name.name)
        if self.state != 'main':
            name_list.append('Back')
        return name_list
        
    def get_page(self, page) -> list | str:
        if page not in self.pages:
            print('page not found')
            return ""

        self.state = page # setting current page
        
        if isinstance(self.pages[page], programs.App): # if the page is a program
            self.startup = True
            return page
        
        #if the page is a string 
        if isinstance(self.pages[page], str):
            print("state is now: ", self.state)
            return self.pages[page]
                
        name_list = []
        for name in self.pages[page]:
            if isinstance(name, str):
                name_list.append(name)
            else:
                name_list.append(name.name)
        if page != 'main':
            name_list.append('Back')

        print('returning: ', name_list)
        
        return name_list

    def get_command(self, command):
        print('setting command: ', command)
        self.last_input = command
    
    def update_program(self):
        if not isinstance(self.pages[self.state], programs.App):
            if self.state == "main":
                self.display.clear()

            self.display.clear()
            self.display.update_frame()
            return
        
        if self.startup:
            self.pages[self.state].restart()
            self.startup = False
        self.pages[self.state].update(self.last_input)
        self.last_input = ""
    

    