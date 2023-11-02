import requests
import cadquery as cq 
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualize_stl(stl_file):
    model_mesh = mesh.Mesh.from_file(stl_file)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(model_mesh.vectors, alpha=0.6, edgecolor="w"))
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_zlim(0, 20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

API_KEY = "39250c09f010b7036f570d85f79cd3f3"

def fetch_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    response = requests.get(base_url.format(city, API_KEY))
    if response.status_code == 200:
        return response.json()["weather"][0]["main"]
    return None

def create_sun():
    sun_core = cq.Workplane("XY").sphere(5)  # Smaller core sphere
    sun_rays = cq.Workplane("XY").pushPoints([(0, 7), (0, -7), (7, 0), (-7, 0),
                                                  (5, 5), (-5, 5), (5, -5), (-5, -5)]).sphere(1)
    sun = sun_core.union(sun_rays)
    sun.exportStl("sun.stl")
    sun.save('sun.stl')

def create_snow():
    # A more intricate snowflake design
    flake = cq.Workplane("XY").lineTo(0, 5).lineTo(1, 4).lineTo(-1, 4).close()
    for _ in range(2):
        flake = flake.revolve(axisStart=(0, 0), axisEnd=(0, 1))
        flake = flake.rotate((0, 0, 0), (0, 0, 1), 60)
    flake.exportStl("snowflake.stl")

def create_cloud():
    # Constructed by unioning several overlapping spheres
    cloud = cq.Workplane("XY").sphere(4)
    cloud_points = [(2, 2, 2), (-2, -2, -1), (-3, 2, 0), (3, -2, 1)]
    for point in cloud_points:
        cloud = cloud.union(cq.Workplane("XY").transformed(offset=point).sphere(3))
    cloud.exportStl("cloud.stl")

def create_rain():
    # Teardrop shaped raindrops
    drop = cq.Workplane("XY").ellipse(1, 1.5).revolve()
    rain = drop
    for i in range(10):
        for j in range(10):
            if i != 0 or j != 0:
                rain = rain.union(drop.transformed(offset=(i*3, j*3, 0)))
    rain.exportStl("rain.stl")

city = input("Enter a city in Norway: ")
weather = fetch_weather(city)

if weather == "Clear":
    create_sun()
    visualize_stl('sun.stl')
elif weather == "Snow":
    create_snow()
    visualize_stl('snowflake.stl')
elif weather == "Clouds":
    create_cloud()
    visualize_stl('cloud.stl')
elif weather == "Rain":
    create_rain()
    visualize_stl('rain.stl')
else:
    print(f"Weather for {city} is {weather}, but no 3D model is available for this condition.")