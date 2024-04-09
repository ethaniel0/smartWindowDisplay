import socketio
import time
import random

link = 'https://a2cc0b4b-ccb1-4a02-87ff-fc39ba6504aa-00-2f7d3zg35rpko.janeway.replit.dev/'

sio = socketio.Client()
connected = False
while not connected:
    try: 
        sio.connect(link)
        connected = True
    except:
        print("Failed to estabolish connection to server: ", link)
        print("Trying again...")
        time.sleep(5)


# @sio.event
# def message(data):
#     print('I received a message: ', data)

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

@sio.on('piJoinCode')
def onpiinit(data):
    print('Pi: ', data)

sio.emit('supersecretpimessage', '3.1415926535897932384626433832769')

while True:
    # msg = input("Enter message: ")
    # print("Sending: ", msg)
    # sio.emit('tryConnect', msg)
    pass

