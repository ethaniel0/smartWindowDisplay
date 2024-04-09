import socketio
import time
import random

#For connecting to the server:
# link = 'https://a2cc0b4b-ccb1-4a02-87ff-fc39ba6504aa-00-2f7d3zg35rpko.janeway.replit.dev/'
link = 'http://localhost:3000/'
sio = socketio.Client()

#program vairables: 
programState = 'start'
display_options = ['Duke Games', 'Weather', 'Games']
game_options = ['Simon', 'Tic Tac Toe', 'Snake', 'Maze']
Simon_options = ['Red', 'Blue', 'Green', 'Yellow']

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
        print("Current display options: ", display_options)
        sio.emit('programList', display_options)

#on disconnect
@sio.event
def disconnect():
    print('disconnected from server')

def main():
    while True:
        if not sio.connected:
            try: 
                sio.connect(link)
                sio.emit('supersecretpimessage', '3.1415926535897932384626433832769')
            except:
                print("Failed to estabolish connection to server: ", link)
                print("Trying again...")
                time.sleep(2)
        pass

if __name__ == '__main__':
    main()

