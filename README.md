# Smart Dorm Display

This project is a smart display for a dorm room. It is designed to be a panel of WS2812B LEDs that can display various information such as the games, Duke Scores and videos.

To drive the panel, a Raspberry Pi 4B is used. The Raspberry Pi runs a socket connection to a server that sends the information to be displayed. The server is a Fly.io server that is running a web interface where users can connect to and send information to the display.

## Electrical

### Pi

The Raspberry Pi is powered by a 5V 3A power supply independent of the LED power supply. The Pi controls the LEDs through a GPIO pin. A fan is also connected to the Pi to keep it cool as part of the case.

### LEDs and Panel

Four strips of WS2812B LEDs are connected to the Pi. The strips are connected in series and a total of 27 columns each with 20 LEDs means that there are 540 LEDs in total. Each panel has 9 such columns and the input and output power lines are shorted such that there is no significant voltage drop accross the panels.

Since the LED strips run in series, the panels can connect in any order and it can be expanded to include any number of panels.

### Power Supply

An on-hand PC power supply was used to power the LEDs. The power supply is rated for 600W, which is overkill, but it is better to have more power than not enough. The power supply is connected to the LEDs through a Mollex connector which runs at 5V.

### Housing

The Pi, power supply, extra cables, connectors, and a small AC power splitter are all stored in a plastic drawer that allows for easy connection and good airflow.

## Software

### LED Driver

### Server

### Web Interface

## Games and Display Pages

### Duke Scores

### Videos

### Simon

### Maze

### Snake