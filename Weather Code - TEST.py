#Test denne, printer blokkbokstaver.

import requests
from stl import mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from text_to_3d import text_to_3d_mesh  # Assume we have a separate module for generating 3D text mesh

# Constants
API_KEY = '39250c09f010b7036f570d85f79cd3f3'  # Replace with your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Ask the user for a city
city = input('Enter a city in Norway: ')

# Fetch weather data from OpenWeatherMap
response = requests.get(f'{BASE_URL}?q={city},NO&appid={API_KEY}')
weather_data = response.json()

# Check for successful response
if response.status_code == 200:
    # Get the main weather condition
    main_condition = weather_data['weather'][0]['main'].upper()
    if main_condition in ['CLEAR', 'CLOUDS', 'SNOW', 'RAIN']:
        condition_map = {'CLEAR': 'SUN', 'CLOUDS': 'CLOUDY', 'SNOW': 'SNOW', 'RAIN': 'RAIN'}
        weather_condition = condition_map[main_condition]
        print(f"The weather in {city} is {weather_condition.lower()}.")
    else:
        print("The weather condition is not one of the specified types.")
else:
    print("Failed to retrieve weather data.")

# Generate 3D mesh from text
weather_mesh = text_to_3d_mesh(weather_condition)

# Create a new plot
figure = plt.figure()
ax = mplot3d.Axes3D(figure)

# Load the STL file and add the vectors to the plot
ax.add_collection3d(mplot3d.art3d.Poly3DCollection(weather_mesh.vectors))

# Auto scale to the mesh size
scale = weather_mesh.points.flatten()
ax.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
plt.show()

# Save the 3D model to an STL file
weather_mesh.save(f'{weather_condition}.stl')