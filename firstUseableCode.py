# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 18:02:40 2023

@author: sande
"""

import requests
import cadquery as cq
from math import sin, cos, radians

# Function to get weather data
def get_weather(city):
    api_key = '39250c09f010b7036f570d85f79cd3f3'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NO&appid={api_key}"
    response = requests.get(url)
    return response.json()

# Function to create a sun model
def create_sun():
    core_height = 4  
    sun_core = cq.Workplane("XY").circle(20).extrude(core_height)  

    x_length = 28  
    y_length = 4  

    # Create rays 
    for angle in range(0, 360, 45):
        ray_profile = (
            cq.Workplane("XY")
            .center(20, 0)  # Position 
            .ellipse(x_length, y_length)
            .extrude(core_height)  # Extrude thickness
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        sun_core = sun_core.union(ray_profile)

    # Export the STL file
    cq.exporters.export(sun_core, "Sun.stl")

# Function to create a rain model
def create_rain(thickness=1.0, scale_factor=3.0):
    # Points to define the profile of the half water drop
    points = [
        (0, 0),  # Bottom of the drop
        (2 * scale_factor, 2 * scale_factor),  # Control point for the curve
        (1 * scale_factor, 4 * scale_factor),  # Top of the curve before the point
        (0, 6 * scale_factor),  # Tip of the drop
    ]

    # Create the water drop 2D profile for one half
    drop_profile = (
        cq.Workplane("XY")
        .moveTo(points[0][0], points[0][1])
        .spline(points[1:], includeCurrent=True)  # Create the spline for the half profile
        .close()  # Close the path to make a proper wire for extrusion
    )

    # Extrude the first half
    half_drop = drop_profile.extrude(thickness)

    # Mirror the half drop along the YZ-axis to create the other half
    other_half_drop = half_drop.mirror("YZ")

    # Combine the two halves to form a complete water drop
    complete_drop = half_drop.union(other_half_drop)

    # Scale the complete water drop by 4 times
    scaled_drop = complete_drop.val().scale(4)

    # Export the scaled complete water drop as an STL file
    cq.exporters.export(scaled_drop, "Rain.stl")

# Function to create a cloud model
def create_cloud():
    # Central ellipsoid to serve as the main body of the cloud
    cloud = cq.Workplane("XY").ellipse(4, 6).extrude(1)

    # Manually defined arrangement of ellipsoids to form the cloud shape, with two removed
    cloud_points = [
        (-5, 1, 0), (6, -2, 0),  # Varied positions for a more natural look
        (0, -6, 0), (7, 3, 0), (-6, -3, 0),
        (3, -5, 0),  (1, 1, 0)
    ]
    ellipsoid_sizes = [
        (2.5, 2), (2.8, 3), (4, 3.5), (3.5, 4), (3, 3.2), 
        (3.1, 3), (5, 3.5), (3.3, 3.2)  # Varied sizes for each ellipsoid (X, Y radii)
    ]

    # Loop to create and union ellipsoids at the defined points and sizes
    for point, (rx, ry) in zip(cloud_points, ellipsoid_sizes):
        ellipsoid = (
            cq.Workplane("XY")
            .transformed(offset=point)
            .ellipse(rx, ry)
            .extrude(1)  # Flatten in the Z-direction
        )
        cloud = cloud.union(ellipsoid)

    # Scale the entire cloud by 4 times
    scaled_cloud = cloud.val().scale(4)

    # Export the scaled compact cloud as an STL file
    cq.exporters.export(scaled_cloud, "Cloud.stl")


# Function to create a snow model (previously named create_pentagon_shape)
def create_snowflake_shape():
    # Function to create an extruded snowflake
    def create_snowflake(radius, height, center=(0, 0)):
        angle = radians(360 / 5)
        points = [
            (center[0] + radius * cos(i * angle), center[1] + radius * sin(i * angle))
            for i in range(5)
        ]
        return cq.Workplane("XY").polyline(points).close().extrude(height)

    # Dimensions
    big_radius = 10
    small_radius = 3
    height = 1
    offset_distance = big_radius + small_radius * 0.6  # Further adjusting distance for overlap
    hole_radius = big_radius * 0.6  # Radius for the larger snowflake hole

    # Create the central large snowflake
    large_snowflake = create_snowflake(big_radius, height)

    # Cut a larger snowflake hole in the center of the large snowflake
    snowflake_hole = create_snowflake(hole_radius, height)
    large_snowflake = large_snowflake.cut(snowflake_hole)

    # Initialize a workplane for smaller snowflakes
    smaller_snowflakes = cq.Workplane("XY")

    # Create and position smaller snowflakes
    for i in range(5):
        angle = radians(i * 72)
        x_offset = offset_distance * cos(angle)
        y_offset = offset_distance * sin(angle)
        smaller_snowflake = create_snowflake(small_radius, height, center=(x_offset, y_offset))
        smaller_snowflakes = smaller_snowflakes.union(smaller_snowflake)

    # Combine the large snowflake with the smaller ones
    combined_shape = large_snowflake.union(smaller_snowflakes)

    # Get the solid and scale it by 4 times
    scaled_shape = combined_shape.val().scale(4)

    # Export the STL file
    cq.exporters.export(scaled_shape, "Snowflake.stl")
# Main function to handle the workflow
def main():
    city = input("Enter a city in Norway (ø = o, æ = ae, å = å): ")
    weather_data = get_weather(city)
    main_weather = weather_data['weather'][0]['main']

    if main_weather == 'Clear':
        create_sun()
        print("It's warm and sunny! Exported as Sun.stl")
    elif main_weather in ['Rain', 'Drizzle']:
        create_rain()
        print("It's a terrible day for rain. Exported as Rain.stl")
    elif main_weather == 'Clouds':
        create_cloud()
        print("Seems cloudy. Exported as Cloud.stl")
    elif main_weather == 'Snow':
        create_snowflake_shape()
        print("Let it snow! Exported as Snowflake.stl")
    else:
        print("Weather condition not recognized.")

if __name__ == "__main__":
    main()
