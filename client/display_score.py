from general_display import Display, to_rgb
from PIL import Image
from urllib import request
import random
import json
import testdisplay

def get_game(json_file = '../duke_scores/data.json'):
    # Returns info for games duke won
    # sport, duke_score, opponent_score, opponent, opponent_logo_url

    with open(json_file) as f:
        data = json.load(f)

    sport = None

    while sport is None or len(data[sport]["scores"]) == 0:
        sport = random.choice(list(data.keys()))

    # Get how many games are in the sport
    num_games = len(data[sport])

    # Do at most 100 iterations
    count = 0
    idx = 0

    while count < 100:
        count += 1
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
            pixel = to_rgb(image.getpixel((i, j))[:3])
            display.set_pixel(i + offset_x, j + offset_y, pixel)

def show_sport(display, sport):

    if "basketball" in sport:
        basketball = [[0, 0, 1, 1, 2, 1, 1, 0, 0],
                      [0, 2, 1, 1, 2, 1, 1, 2, 0],
                      [1, 1, 2, 1, 2, 1, 2, 1, 1],
                      [1, 1, 2, 1, 2, 1, 2, 1, 1],
                      [1, 1, 2, 2, 2, 2, 2, 1, 1],
                      [1, 1, 2, 1, 2, 1, 2, 1, 1],
                      [1, 1, 2, 1, 2, 1, 2, 1, 1],
                      [0, 2, 1, 1, 2, 1, 1, 2, 0],
                      [0, 0, 1, 1, 2, 1, 1, 0, 0]]
        for i in range(9):
            for j in range(9):
                if basketball[j][i] == 1:
                    display.set_pixel(i + 9, j + 6, to_rgb((242, 134, 2)))
                elif basketball[j][i] == 2:
                    display.set_pixel(i + 9, j + 6, to_rgb((50, 50, 50)))

    elif "football" in sport:
        football = [[0, 0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 0, 0],
                    [0, 0, 1, 1, 2, 1, 1, 1, 0],
                    [0, 0, 1, 2, 2, 2, 1, 1, 0],
                    [0, 1, 1, 1, 2, 1, 1, 1, 1],
                    [0, 1, 1, 2, 2, 2, 1, 1, 1],
                    [0, 1, 1, 1, 2, 1, 1, 1, 1],
                    [0, 1, 1, 2, 2, 2, 1, 1, 1],
                    [0, 0, 1, 1, 2, 1, 1, 1, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 0, 0]]
        for i in range(9):
            for j in range(12):
                if football[j][i] == 1:
                    display.set_pixel(i + 9, j + 4, to_rgb((94, 49, 1)))
                elif football[j][i] == 2:
                    display.set_pixel(i + 9, j + 4, to_rgb((255, 255, 255)))
    
    elif "lacrosse" in sport:
        lacrosse = [[0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 1, 0, 0, 2, 0, 0, 1, 0],
                    [0, 1, 2, 2, 2, 2, 2, 1, 0],
                    [0, 1, 0, 0, 2, 0, 0, 1, 0],
                    [0, 1, 1, 2, 2, 2, 1, 1, 0],
                    [0, 0, 1, 0, 2, 0, 1, 0, 0],
                    [0, 0, 1, 2, 2, 2, 1, 0, 0],
                    [0, 0, 1, 0, 2, 0, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 3, 1, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0]]
        for i in range(9):
            for j in range(16):
                if lacrosse[j][i] == 1:
                    display.set_pixel(i + 9, j + 3, to_rgb((2, 37, 209)))
                elif lacrosse[j][i] == 2:
                    display.set_pixel(i + 9, j + 3, to_rgb((255, 255, 255)))
                elif lacrosse[j][i] == 3:
                    display.set_pixel(i + 9, j + 3, to_rgb((255, 255, 255)))

    elif "baseball" in sport:
        baseball = [[0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 2, 1, 1, 1, 1, 1, 2, 0],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [0, 2, 1, 1, 1, 1, 1, 2, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0, 0]]
         
        for i in range(9):
            for j in range(9):
                if baseball[j][i] == 1:
                    display.set_pixel(i + 9, j + 6, to_rgb((255, 255, 255)))
                elif baseball[j][i] == 2:
                    display.set_pixel(i + 9, j + 6, to_rgb((255, 0, 0)))

    elif "tennis" in sport:
        baseball = [[0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 2, 1, 1, 1, 1, 1, 2, 0],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [1, 1, 2, 1, 1, 1, 2, 1, 1],
                    [0, 2, 1, 1, 1, 1, 1, 2, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0, 0]]
         
        for i in range(9):
            for j in range(9):
                if baseball[j][i] == 1:
                    display.set_pixel(i + 9, j + 6, to_rgb((98, 191, 55)))
                elif baseball[j][i] == 2:
                    display.set_pixel(i + 9, j + 6, to_rgb((255, 255, 255)))

    elif "soccer" in sport:
        soccerball = [[0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 1, 2, 2, 2, 1, 0, 0],
                      [0, 1, 2, 2, 1, 2, 2, 1, 0],
                      [1, 2, 2, 1, 1, 1, 2, 2, 1],
                      [1, 2, 1, 1, 1, 1, 1, 2, 1],
                      [1, 2, 1, 1, 1, 1, 1, 2, 1],
                      [0, 1, 2, 1, 1, 1, 2, 1, 0],
                      [0, 0, 1, 2, 2, 2, 1, 0, 0],
                      [0, 0, 0, 1, 1, 1, 0, 0, 0]]
        
        for i in range(9):
            for j in range(9):
                if soccerball[j][i] == 1:
                    display.set_pixel(i + 9, j + 6, to_rgb((50, 50, 50)))
                elif soccerball[j][i] == 2:
                    display.set_pixel(i + 9, j + 6, to_rgb((255, 255, 255)))

    else:
        return


def show_Duke_logo(display: Display):
    # Puts the Duke logo on the display: grid is 9x8
    offset_x, offset_y = 0, 1

    pixels = [[1, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1, 1, 1, 0],
              [1, 1, 1, 1, 1, 1, 1, 0, 0]]

    for i in range(9):
        for j in range(8):
            if pixels[j][i] == 1:
                display.set_pixel(i + offset_x, j + offset_y, to_rgb((0, 0, 255)))

def place_url(display, url, img_size = (7, 7), offset = (9, 1)):

    request.urlretrieve(url, "temp.png")

    image = Image.open("temp.png")
    image = image.resize(img_size)

    offset_x, offset_y = offset

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            pixel = to_rgb(image.getpixel((i, j))[:3])
            display.set_pixel(i + offset_x, j + offset_y, pixel)

    # os.remove("temp.png")
    
def show_number(display, num, window, color = (255, 0, 0)):
    offset_x = 9 * window
    y = 12
    num_ones = num % 10
    num_tens = num // 10 % 10
    num_hundreds = num // 100

    if num_hundreds != 0:
        display.show_digit(num_hundreds, color, 0 + offset_x, y)
        display.show_digit(num_tens, color, 3 + offset_x, y)
        display.show_digit(num_ones, color, 6 + offset_x, y)
    elif num_tens != 0:
        display.show_digit(num_tens, color, 1 + offset_x, y)
        display.show_digit(num_ones, color, 5 + offset_x, y)
    else:
        display.show_digit(num_ones, color, 3 + offset_x, y)

def show_random_game(display):
    json_file = '../duke_scores/data.json'

    sport, duke_score, opponent_score, opponent, opponent_logo_url = get_game(json_file)
    print(f"Duke won a {sport} game against {opponent} with a score of {duke_score}-{opponent_score}")

    show_Duke_logo(display)
    show_number(display, duke_score, 0, color = (0, 0, 255))

    show_sport(display, sport)

    place_url(display, opponent_logo_url, img_size=(9, 9), offset = (9*2, 1))
    show_number(display, opponent_score, 2)

    display.show()


if __name__ == "__main__":
    display = testdisplay.TestDisplay()
    json_file = '../duke_scores/data.json'
    show_random_game(display)
    display.mainloop()


