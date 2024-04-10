import testdisplay
from PIL import Image
from urllib import request
import os
import random
import json


display = testdisplay.TestDisplay()

json_file = '../duke_scores/data.json'


def get_game():
    # Returns info for games duke won
    # sport, duke_score, opponent_score, opponent, opponent_logo_url

    with open(json_file) as f:
        data = json.load(f)

    sport = random.choice(list(data.keys()))

    # Get how many games are in the sport
    num_games = len(data[sport])

    # Get a random game (keep going until we find a game duke won)
    # Do at most 100 iterations
    count = 0
    idx = 0
    while count < 100:
        idx = random.randint(0, num_games - 1)
        # Check that Duke won by indexing into the "scores" list within the sport
        if len(data[sport]["scores"]) <= idx:
            continue
        scores = data[sport]["scores"][idx]
        # Scores is smoething like "4-3" with Duke first
        scores = scores.split("-")
        duke_score = int(scores[0])
        opponent_score = int(scores[1])
        if duke_score > opponent_score:
            break

    # If Duke as somehow winless in the sport
    if count >= 100:
        return get_game()

    return sport, duke_score, opponent_score, data[sport]["opponents"][idx], data[sport]["logos"][idx]




def place_img(f, img_size = (7, 7), offset = (9, 1)):

    offset_x, offset_y = offset

    image = Image.open(f)
    image = image.resize(img_size)

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            pixel = testdisplay.to_rgb(image.getpixel((i, j))[:3])
            display.set_pixel(i + offset_x, j + offset_y, pixel)

def place_w():
    # Puts a green W on the display

    offset_x, offset_y = 10, 10

    display.set_pixel(0 + offset_x, 2 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(0 + offset_x, 3 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(0 + offset_x, 4 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(1 + offset_x, 5 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(2 + offset_x, 6 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(3 + offset_x, 5 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(3 + offset_x, 4 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(4 + offset_x, 6 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(5 + offset_x, 5 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(6 + offset_x, 4 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(6 + offset_x, 3 + offset_y, testdisplay.to_rgb((0, 255, 0)))
    display.set_pixel(6 + offset_x, 2 + offset_y, testdisplay.to_rgb((0, 255, 0)))
 
def place_url(url, img_size = (7, 7), offset = (9, 1)):

    request.urlretrieve(url, "temp.png")

    image = Image.open("temp.png")
    image = image.resize(img_size)

    offset_x, offset_y = offset

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            pixel = testdisplay.to_rgb(image.getpixel((i, j))[:3])
            display.set_pixel(i + offset_x, j + offset_y, pixel)

    os.remove("temp.png")
    

sport, duke_score, opponent_score, opponent, opponent_logo_url = get_game()

print(f"Duke won a {sport} game against {opponent} with a score of {duke_score}-{opponent_score}")

# place_img('img/balls/basketball.png', offset = (10, 1))
# place_w()

# place_img('img/logos/duke.png', img_size=(15, 15), offset = (1, 1))
place_url(opponent_logo_url, img_size=(20, 20), offset = (0, 0))

display.mainloop()


