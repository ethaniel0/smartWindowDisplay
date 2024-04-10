import json
import os


def get_data():
    data = {}
    for folder in os.listdir('data'):
        with open(f'data/{folder}/logos.txt') as f:
            logos = f.read().splitlines()
        with open(f'data/{folder}/opponents.txt') as f:
            opponents = f.read().splitlines()
        with open(f'data/{folder}/scores.txt') as f:
            scores = f.read().splitlines()
        data[folder] = {
            'logos': logos,
            'opponents': opponents,
            'scores': scores
        }
    return data


def convert_to_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def main():
    data = get_data()
    convert_to_json(data)


if __name__ == '__main__':
    main()
