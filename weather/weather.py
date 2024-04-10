import requests
import json

token_file = 'token.txt'

def get_weather():
    with open(token_file) as f:
        token = f.read().strip()
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Durham,us&appid={token}'
    response = requests.get(url)
    data = response.json()
    return data

def convert_to_json(data):
    with open('weather.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():
    data = get_weather()
    convert_to_json(data)

if __name__ == '__main__':
    main()