# Smart Dorm Display

This project is a smart display for a dorm room. It is designed to be a panel of WS2812B LEDs that can display various information such as the games, Duke Scores and videos.

To drive the panel, a Raspberry Pi 4B is used. The Raspberry Pi runs a socket connection to a server that sends the information to be displayed. The server is a Fly.io server that is running a web interface where users can connect to and send information to the display.

## Electrical

### Pi

The Raspberry Pi is powered by a 5V 3A power supply independent of the LED power supply. The Pi controls the LEDs through a GPIO pin. A fan is also connected to the Pi to keep it cool as part of the case.

### LEDs and Panel

Four strips of WS2812B LEDs are connected to the Pi. The strips are connected in series and a total of 27 columns each with 20 LEDs means that there are 540 LEDs in total. Each panel has 9 such columns and the input and output power lines are shorted such that there is no significant voltage drop across the panels.

Since the LED strips run in series, the panels can connect in any order and it can be expanded to include any number of panels.

### Power Supply

An on-hand PC power supply was used to power the LEDs. The power supply is rated for 600W, which is overkill, but it is better to have more power than not enough. The power supply is connected to the LEDs through a Mollex connector which runs at 5V.

### Housing

The Pi, power supply, extra cables, connectors, and a small AC power splitter are all stored in a plastic drawer that allows for easy connection and good airflow.

## Software

### LED Driver

The role of the LED driver is to create a simple but useful abstraction between X-Y coordinates and the LEDs. The driver is written in Python and uses the `rpi_ws281x` library to control the LEDs. Further, it is initialized with parameters such as the number of LEDs, the number of columns, the wiring pattern to control the LEDs, and the brightness of the LEDs.

It includes functions to set the color of a single LED, a column, a row, or the entire panel. It also includes functions to clear the panel, set the brightness, and update the LEDs.

### Pi Software

The main program running on the Pi is a Python script. It connects to the server using socketio in Python 3.12. As socketio is multithreaded, messages sent from Socketio set flags in the code to signal updates to the display, which runs in the main thread. We use a custom program manager to control and update the current running application, as well as to navigate between programs. All “apps” are standardized to contain reset and update methods, which are called when starting the program and during the update routine. Each app is provided access to the LED driver to control what happens on screen.
 	
The whole system is run on boot. It is important to note that to control the LEDs, the program must be run as root. This is done by running the program as a cron job through the root user.

#### Challenges with Python 3.12 and Ubuntu 20.04 
It is well-known that Python 3.12 does not play well on Ubuntu 20.04. However, the socket.io Python features used are specific to Python 3.12. Further, the `rpi_ws281x` library is also implicitly specific to Python 3.11 since the internally used RPi.GPIO library is not officially supported on Python 3.12.

The solution to this problem would be best solved with a Docker container or a virtual environment. However, for simplicity and speed, the solution was just to use a few symbolic links to the Python 3.12 libraries.

### Server

Our server uses NodeJS as its backend. It uses express.js to serve the webpage statically, and the socket.io module connects to the server to intercept web socket messages. The server keeps global client and server variables, which are updated when the pi or a user connects. For the Raspberry Pi to connect, it must send a post request to a specific route, with the password in the body of the socket message. If the password is correct, the pi global variable is set. On disconnect, the variable becomes null. When the user connects, a message is sent to the pi to obtain the join code, which is also desplayed on our display. If the right join code is entered, the client global variable is set. On disconnect (such as page reload), the client variable is set to null.

When both client and pi are connected, the server connects any messages from either side to the other. Messages from each are only relayed if the user and pi are the ones kept in the global variables.

The server is deployed on fly.io.

### Web Interface
The website is a static HTML/CSS/JS site. The default screen is a connect button that will alert the user if the Pi has been disconnected or another user is already connected. Each game / program is kept in a div that's hidden (with CSS) until it's selected. The javascript sends and receives messages to connect and send the join code, as well as to navigate the applications and send commands for each application. These are chosen based on button inputs set in the HTML. Different applications can reuse the same gamepads if needed, which simplifies our logic.

## Games and Display Pages

### Duke Scores

Obtaining the Duke scores is done through a web scraper that scrapes the Duke Athletics website (goduke.com). The scraper is written as a bash script and generates a json. Therefore, the script only needs to be run once a day to get the scores for the day.

Further, the script is designed so that it can get data for all applicable sports (tennis, football, lacrosse, soccer, etc.) and not just basketball. It internally uses `wget` to download the page and `grep` to find the relevant information with `sed` to perform regex operations.

The Duke scores are displayed across the three pannels with Duke on the left, the sport type in the middle, and the opponent on the right. The score are displayed below their respective teams. The Duke D and sport type displayed are preprogrammed images to fit the pixelated layout, but the opponent's logo is scraped from the website.

### Videos
Videos for thisplay are generated using a separate python script. The script uses OpenCV to read each frame from the video and resize it to the resolution of the display (27x20), and then appends the frame as a numpy array to a running list. That list is then pickled as a .pkl file (turned into a binary using Python's pickle library). Once in this format, the .pkl file can be loaded into a VideoPlayer application instance and run. The VideoPlayer simply reads each frame one-by-one and displays each pixel in the frame. Frames are updated 30 times a second.

### Simon
Simon is the classic game we've all played. On the display, it starts with a blinking line, which disappears once the user presses start. From there, it goes back and forth between adding a color and displaying it, and collecting each user input to verify the user remembered the sequence. If the user enters the wrong sequence, the game ends and you can always start again.

### Maze
Maze is built to randomly generate a maze and have the user navigate through it. It utilizes a depth-first search algorithm with backtracking to generate the maze so that it is always solvable. When the user inputs "up", "down", "left", or "right", the display will update to show the user's position in the maze, creating a light green trail behind it so that they can see where they have been. 
For each randomly generated maze, the start will always be in the top left and the end will always be in the bottom right. When a user finishes the maze, they are rewarded with a new random maze so that they can have endless fun solving mazes. 

 ### Snake
Snake is built to be the classic game where the user controls a snake that grows as it eats food. The snake moves in the direction the user inputs, and the user can change the direction of the snake by inputting "up", "down", "left", or "right". The user can start the game by inputting any control and setting the initial heading of the snake. 
The snake will grow in length as it eats food, and the game will end if the snake runs into itself or the wall. Once the game ends, a new randomly generated position of the snake and food will be generated so that the user can play again. 

### Jump 
Jump is built to be a simple game where the user controls a character that jumps over and ducks under obstacles. The user can control the character by inputting "up" to jump and "down" to duck. The character will avoid obstacles that are randomly generated on the screen. The game will end if the character runs into an obstacle. The user starts the game by pressing "start" and can play again by pressing "start" after the game ends.
