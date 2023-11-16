#DENNE SKAL FUNKE; 

import requests

def get_weather(city):
    api_key = '39250c09f010b7036f570d85f79cd3f3'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NO&appid={api_key}"
    response = requests.get(url)
    return response.json()

def select_stl_file(weather_data):
    main_weather = weather_data['weather'][0]['main']
    if main_weather == 'Clear':
        return 'path/to/sun.stl'
    elif main_weather == 'Rain' or main_weather == 'Drizzle':
        return 'path/to/rain.stl'
    elif main_weather == 'Snow':
        return 'path/to/snow.stl'
    else:
        return 'path/to/cloud.stl'

def save_stl_file(file_path, save_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    with open(save_path, 'wb') as file:
        file.write(content)
    print(f"STL file saved as {save_path}")

def main():
    city = input("Enter a city in Norway: ")
    weather_data = get_weather(city)
    stl_file_path = select_stl_file(weather_data)
    save_path = 'your/desired/save/location/output.stl'
    save_stl_file(stl_file_path, save_path)

if __name__ == "__main__":
    main()
