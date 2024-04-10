import socketio
import programs
import testdisplay

class ProgramManager:
    def __init__(self, sio: socketio.Client):
        self.state = "main"
        self.sio = sio
        self.display = testdisplay.TestDisplay()
        
        self.pages = {
            "main": ["Duke Game", "Weather", "Games"],
            "Games": ["Simon", "Snake", "Maze"],
            
            "Simon": programs.Simon(sio, self.display),
            "Snake": programs.Snake(sio, self.display),
            "Maze": programs.Maze(sio, self.display),
        }
        
        self.last_input = ""
        self.startup = False
        
    
    def go_one_page_up(self):
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
            return ""

        self.state = page
        if isinstance(self.pages[page], programs.App):
            app: programs.App = self.pages[page]
            self.startup = True
            return page
        
        name_list = []
        for name in self.pages[page]:
            if isinstance(name, str):
                name_list.append(name)
            else:
                name_list.append(name.name)
        if page != 'main':
            name_list.append('Back')
        
        return name_list

    def get_command(self, command):
        print('setting command: ', command)
        self.last_input = command
    
    def update_program(self):
        if not isinstance(self.pages[self.state], programs.App):
            return
        if self.startup:
            self.pages[self.state].restart()
            self.startup = False
        self.pages[self.state].update(self.last_input)
        self.last_input = ""
    

    