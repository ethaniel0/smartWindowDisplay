import socketio
import time
import random
import program_manager
import display_score
import time
import testdisplay
from threading import Semaphore

#For connecting to the server:
# link = 'https://a2cc0b4b-ccb1-4a02-87ff-fc39ba6504aa-00-2f7d3zg35rpko.janeway.replit.dev/'
link = 'http://localhost:3000/'
# link = 'https://smartdormdisplay.fly.dev'
sio = socketio.Client()
piDisplay = testdisplay.TestDisplay()

manager = program_manager.ProgramManager(sio, piDisplay)
join_code = [] 
display_numbers_flag = False
connected_to_device_flag = False

globalSem = Semaphore()

press = False
gameCommand = False
static_screen = False


#Pi Messages:
@sio.on('tryConnect')
def on_message():
    global display_numbers_flag, join_code
    randint1 = random.randint(0, 9)
    randint2 = random.randint(0, 9)
    randint3 = random.randint(0, 9)
    print('Sending over the numbers: ', randint1, randint2, randint3)
    numstring = str(randint1) + str(randint2) + str(randint3)
    sio.emit('piJoinCode', numstring)
    join_code = [randint1, randint2, randint3]
    display_numbers_flag = True

@sio.on('supersecretpimessage')
def onpiinit(data):
    print('Pi connected: ', data)

@sio.on('joinCode')
def on_join(data):
    global connected_to_device_flag
    print('Joined: ', data)
    if data == 'success':
        options = manager.get_page(manager.state)
        sio.emit('programList', options)
        connected_to_device_flag = True
        
@sio.on('userGone')
def on_user_gone():
    global connected_to_device_flag
    print('User MIA')
    connected_to_device_flag = False
        
@sio.on('press')
def press_item(data):
    global press
    globalSem.acquire()
    press = data
    globalSem.release()

@sio.on('gameCommand')
def game_command(data):
    global gameCommand
    globalSem.acquire()
    gameCommand = data
    globalSem.release()
    print('Command: ', data)
    # manager.get_command(data)
            
#on disconnect
@sio.event
def disconnect():
    print('Disconnected from server')

def display_large_number(num, section):
    #section 1 is the left section (0-8), section 2 is the middle section (9-17), section 3 is the right section (18-26)
    if section == 1:
        for i in range(5):
            for j in range(3):
                if piDisplay.digits[num][i][j] == 1:
                    piDisplay.set_pixel(j + 3, i + 7, testdisplay.to_rgb((218,154,230)))
    elif section == 2:
        for i in range(5):
            for j in range(3):
                if piDisplay.digits[num][i][j] == 1:
                    piDisplay.set_pixel(j + 12, i  + 7, testdisplay.to_rgb((173,50,173)))
    elif section == 3:
        for i in range(5):
            for j in range(3):
                if piDisplay.digits[num][i][j] == 1:
                    piDisplay.set_pixel(j + 21, i  + 7, testdisplay.to_rgb((148,3,148)))
    else:
        print("Invalid section number")
    print("Displaying number: ", num, " in section: ", section)
    

def main():
    global display_numbers_flag, join_code, press, gameCommand
    piDisplay.fill_with_digits((3,42,148))
    piDisplay.update_frame()
    while True:
        if not sio.connected:
            try: 
                sio.connect(link)
                sio.emit('supersecretpimessage', '3.1415926535897932384626433832769')
            except:
                print("Failed to estabolish connection to server: ", link)
                print("Trying again...")
                time.sleep(2)
        
        if display_numbers_flag:
            piDisplay.clear()
            piDisplay.set_all_pixels((3, 42, 148))
            display_large_number(join_code[0], 1)
            display_large_number(join_code[1], 2)
            display_large_number(join_code[2], 3)
            piDisplay.update_frame()
            display_numbers_flag = False
        
        if sio.connected and connected_to_device_flag:
            
            if press:
                globalSem.acquire()
                print("Press: ", press)
                if press == 'Back':
                    options = manager.go_one_page_up()
                    sio.emit('programList', options)
                else:
                    options = manager.get_page(press)
                    if options == '':
                        sio.emit('programList', ['Back'])
                    sio.emit('programList', options)
                press = False
                globalSem.release()
            elif gameCommand:
                globalSem.acquire()
                manager.get_command(gameCommand)
                gameCommand = False
                globalSem.release()
                
            manager.update_program()
            


if __name__ == '__main__':
    main()

