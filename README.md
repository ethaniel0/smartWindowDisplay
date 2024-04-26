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

It is well-known that Python 3.12 does not play well on Ubuntu 20.04. However, the socket.io Python features used are specific to Python 3.12. Further, the `rpi_ws281x` library is also implicitly specific to Python 3.11 since the internally used RPi.GPIO library is not officially supported on Python 3.12.

The solution to this problem would be best solved with a Docker container or a virtual environment. However, for simplicity and speed, the solution was just to use a few symbolic links to the Python 3.12 libraries.

The whole system is run on boot. It is important to note that to control the LEDs, the program must be run as root. This is done by running the program as a cron job through the root user.

### Server

### Web Interface

## Games and Display Pages

### Duke Scores

Obtaining the Duke scores is done through a web scraper that scrapes the Duke Athletics website (goduke.com). The scraper is written as a bash script and generates a json. Therefore, the script only needs to be run once a day to get the scores for the day.

Further, the script is designed so that it can get data for all applicable sports (tennis, football, lacrosse, soccer, etc.) and not just basketball. It internally uses `wget` to download the page and `grep` to find the relevant information with `sed` to perform regex operations.

TODO Lilly

### Videos

### Simon

### Maze

### Snake