import socketio
import time
import random
import program_manager
import time

#For connecting to the server:
link = 'https://a2cc0b4b-ccb1-4a02-87ff-fc39ba6504aa-00-2f7d3zg35rpko.janeway.replit.dev/'
# link = 'http://localhost:3000/'
sio = socketio.Client()

manager = program_manager.ProgramManager(sio)

#Pi Messages:

@sio.on('tryConnect')
def on_message():
    randint1 = random.randint(0, 9)
    randint2 = random.randint(0, 9)
    randint3 = random.randint(0, 9)
    randint4 = random.randint(0, 9)
    print('Sending over the numbers: ', randint1, randint2, randint3, randint4)
    numstring = str(randint1) + str(randint2) + str(randint3) + str(randint4)
    sio.emit('piJoinCode', numstring)

@sio.on('supersecretpimessage')
def onpiinit(data):
    print('Pi connected: ', data)

@sio.on('joinCode')
def on_join(data):
    print('Joined: ', data)
    if data == 'success':
        options = manager.get_page(manager.state)
        sio.emit('programList', options)
        
@sio.on('press')
def press_item(data):
    print('Pressed: ', data)
    if data == 'Back':
        options = manager.go_one_page_up()
        sio.emit('programList', options)
    else:
        options = manager.get_page(data)
        if options == '':
            sio.emit('programList', ['Back'])
        sio.emit('programList', options)
            
#on disconnect
@sio.event
def disconnect():
    print('Disconnected from server')

def main():
    last_time = time.time()
    update_frequency = 0.1
    last_time = time.perf_counter()
    while True:
        if not sio.connected:
            try: 
                sio.connect(link)
                sio.emit('supersecretpimessage', '3.1415926535897932384626433832769')
            except:
                print("Failed to estabolish connection to server: ", link)
                print("Trying again...")
                time.sleep(2)
        
        if (time.perf_counter() - last_time) > update_frequency:
            last_time = time.perf_counter()
            manager.update_program()

if __name__ == '__main__':
    main()

