%Initial Kode - Vær - Mangler Ordentlige værsymboler
%Spørsmål; "Kan vi importere STL filer istedetfor å be programmet lage de?"

import requests
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualize_stl(stl_file):
    # Load the STL file using numpy-stl
    model_mesh = mesh.Mesh.from_file(stl_file)

    # Create a new plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Draw the STL mesh
    ax.add_collection3d(Poly3DCollection(model_mesh.vectors, alpha=0.6, edgecolor="w"))

    # Setting the aspect ratio, limits, and labels
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_zlim(0, 20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Display the plot
    plt.show()



API_KEY = "39250c09f010b7036f570d85f79cd3f3"


def fetch_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    response = requests.get(base_url.format(city, API_KEY))
    if response.status_code == 200:
        return response.json()["weather"][0]["main"]
    return None


def create_sun():
    # A basic sun represented by a sphere
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, np.pi, 25)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    sun = mesh.Mesh(np.zeros(x.shape[0] * x.shape[1], dtype=mesh.Mesh.dtype))
    for i in range(x.shape[1]):
        for j in range(x.shape[0]):
            sun.vectors[i * x.shape[0] + j] = [[x[j, i], y[j, i], z[j, i]],
                                               [x[(j + 1) % x.shape[0], i], y[(j + 1) % x.shape[0], i],
                                                z[(j + 1) % x.shape[0], i]],
                                               [x[j, (i + 1) % x.shape[1]], y[j, (i + 1) % x.shape[1]],
                                                z[j, (i + 1) % x.shape[1]]]]

    sun.save('sun.stl')

def create_snow():
    # A basic snowflake represented by three crossed rods
    length = 10
    diameter = 1
    points = np.array([
        [-length/2, 0, 0],
        [length/2, 0, 0],
        [0, -length/2, 0],
        [0, length/2, 0],
        [0, 0, -length/2],
        [0, 0, length/2]
    ])

    rods = [
        [points[0], points[1]],
        [points[2], points[3]],
        [points[4], points[5]]
    ]

    snowflake = mesh.Mesh(np.zeros(6, dtype=mesh.Mesh.dtype))
    for i, rod in enumerate(rods):
        snowflake.vectors[2*i] = [rod[0], [rod[0][0], rod[0][1], rod[0][2] + diameter], [rod[0][0] + diameter, rod[0][1], rod[0][2]]]
        snowflake.vectors[2*i + 1] = [rod[1], [rod[1][0], rod[1][1], rod[1][2] + diameter], [rod[1][0] + diameter, rod[1][1], rod[1][2]]]

    snowflake.save('snowflake.stl')


def create_cloud():
    # A basic cloud represented by a squashed sphere
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, np.pi, 25)
    x = 15 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 5 * np.outer(np.ones(np.size(u)), np.cos(v))

    cloud = mesh.Mesh(np.zeros(x.shape[0] * x.shape[1], dtype=mesh.Mesh.dtype))
    for i in range(x.shape[1]):
        for j in range(x.shape[0]):
            cloud.vectors[i * x.shape[0] + j] = [[x[j, i], y[j, i], z[j, i]],
                                                 [x[(j + 1) % x.shape[0], i], y[(j + 1) % x.shape[0], i],
                                                  z[(j + 1) % x.shape[0], i]],
                                                 [x[j, (i + 1) % x.shape[1]], y[j, (i + 1) % x.shape[1]],
                                                  z[j, (i + 1) % x.shape[1]]]]

    cloud.save('cloud.stl')


def create_rain():
    # A simple rain depiction using vertical rods
    number_of_drops = 50
    drop_length = 8
    drop_radius = 0.2
    spacing = 3  # Space between drops

    # Initialize the rain mesh
    rain = mesh.Mesh(np.zeros(number_of_drops * 2, dtype=mesh.Mesh.dtype))

    for i in range(number_of_drops):
        x = (i % int(np.sqrt(number_of_drops))) * spacing
        y = (i // int(np.sqrt(number_of_drops))) * spacing
        z = 0

        top_point = [x, y, z + drop_length]
        bottom_point = [x, y, z]
        side_point_1 = [x + drop_radius, y, z]
        side_point_2 = [x, y + drop_radius, z]

        # Define the two triangles that make up each rod in the raindrop
        rain.vectors[2 * i] = [top_point, bottom_point, side_point_1]
        rain.vectors[2 * i + 1] = [top_point, bottom_point, side_point_2]

    rain.save('rain.stl')

def main():
    city = input("Enter the city name: ")
    weather = fetch_weather(city)

    if weather == "Clear":
        create_sun()
        print("Created 3D model for Sun.")
        visualize_stl('sun.stl')
    elif weather == "Clouds":
        create_cloud()
        print("Created 3D model for Clouds.")
        visualize_stl('cloud.stl')
    elif weather == "Snow":
        create_snow()
        print("Created 3D model for Snow.")
        visualize_stl('snowflake.stl')
    # Additional conditions for rain (once you create that function)
    # ...
    elif weather == "Rain":
        create_rain()
        print("Created 3D model for Rain.")
        visualize_stl('rain.stl')
    else:
        print(f"Weather in {city} is {weather}, no model generated.")



if __name__ == "__main__":
    main()

