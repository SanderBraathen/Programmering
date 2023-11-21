# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 15:35:45 2023

@author: sande
"""

#WEATHER API CODE: 

import tkinter as tk #Imported to create a friendly user interface. 
from tkinter import messagebox, ttk
import threading
import requests
import cadquery as cq
from math import sin, cos, radians

# function to get weather data
def get_weather(city):
    api_key = '39250c09f010b7036f570d85f79cd3f3'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NO&appid={api_key}"
    response = requests.get(url)
    return response.json()

# some scaling used because some models didn't behave themselves otherwise

# function to create sun model
# core disc with rays shooting out
def create_sun():
    coreHeight = 4  
    sunCore = cq.Workplane("XY").circle(20).extrude(coreHeight)  

    x_length = 28  
    y_length = 4  
   
    for rays in range(0, 360, 45):
        rayProfile = (
            cq.Workplane("XY")
            .center(20, 0)   
            .ellipse(x_length, y_length)
            .extrude(coreHeight)  
            .rotate((0, 0, 0), (0, 0, 1), rays)
        )
        sunCore = sunCore.union(rayProfile)

    cq.exporters.export(sunCore, "Sun.stl")

# function to create a raindrop model for rain, drizzle
# harder geometry, decided to make a half drop and mirror it
def create_rain(thickness=1.0, scaleFactor=3.0):
    points = [
        (0, 0),  
        (2 * scaleFactor, 2 * scaleFactor),  
        (1 * scaleFactor, 4 * scaleFactor),  
        (0, 6 * scaleFactor),  
    ]
    drop_profile = (
        cq.Workplane("XY")
        .moveTo(points[0][0], points[0][1])
        .spline(points[1:], includeCurrent=True)  
        .close()  
    )
  
    halfDrop = drop_profile.extrude(thickness)

    
    otherHalf = halfDrop.mirror("YZ")
    fullDrop = halfDrop.union(otherHalf)
    scaledDrop = fullDrop.val().scale(4)

    cq.exporters.export(scaledDrop, "Rain.stl")

# function to create cloud model
# just semi-randomly placed and sized elipses to serve as a cloud, unified
def create_cloud():
    cloud = cq.Workplane("XY").ellipse(4, 6).extrude(1)

    cloudPoints = [
        (-5, 1, 0), (6, -2, 0), (0, -6, 0), (7, 3, 0), (-6, -3, 0),(3, -5, 0), (1, 1, 0)
        ]
    
    sizes = [
        (2.5, 2), (2.8, 3), (4, 3.5), (3.5, 4), (3, 3.2), (3.1, 3), (5, 3.5), (3.3, 3.2)
        ]

    
    for point, (rx, ry) in zip(cloudPoints, sizes):
        fixShape = (
            cq.Workplane("XY")
            .transformed(offset=point)
            .ellipse(rx, ry)
            .extrude(1) 
        )
        cloud = cloud.union(fixShape)

    
    scaledCloud = cloud.val().scale(4)

    cq.exporters.export(scaledCloud, "Cloud.stl")

# function to create snowflake for snowy weather
# pentagons with smaller pentagons in the corners to look like a snowflake
def create_snow():
    def create_snowflake(rad, ht, ctr=(0, 0)): # nested function for ease of calling later
        pts = []
        step = 360 / 5
        for i in range(5):
            aDeg = step * i
            aRad = radians(aDeg)
            x = ctr[0] + rad * cos(aRad)
            y = ctr[1] + rad * sin(aRad)
            pts.append((x, y))
        return cq.Workplane("XY").polyline(pts).close().extrude(ht)

    bigSnowRad = 10
    smallSnowRad = 3
    snowHeight = 1
    gap = bigSnowRad + smallSnowRad * 0.6 
    holeRad = bigSnowRad * 0.6  

    bigSnow = create_snowflake(bigSnowRad, snowHeight)
    middleSnow = create_snowflake(holeRad, snowHeight)
    bigSnow = bigSnow.cut(middleSnow)

    snowPieces = cq.Workplane("XY")

    for i in range(5):
        rot = i * 72
        rotRad = radians(rot)
        xGap = gap * cos(rotRad)
        yGap = gap * sin(rotRad)
        tinySnow = create_snowflake(smallSnowRad, snowHeight, ctr=(xGap, yGap))
        snowPieces = snowPieces.union(tinySnow)

    finalSnowflake = bigSnow.union(snowPieces)
    scaledSnowflake = finalSnowflake.val().scale(4)

    cq.exporters.export(scaledSnowflake, "Snowflake.stl")

# layout of UI
def enhance_ui(root):
    def create_button(text, action, container):
        btn = ttk.Button(container, text=text, command=action)
        btn.pack(pady=5)
        return btn

    root.title("3D Model Generator - Norway")
    root.geometry("400x200")  # Set the window size

    style = ttk.Style(root)
    style.theme_use("alt")  # Use a different theme

    label_header = ttk.Label(root, text="Generate Your 3D Model", font=("Arial", 16))
    label_header.pack(pady=10)

    frame_city_input = ttk.Frame(root)
    frame_city_input.pack(pady=5, padx=10, fill=tk.X)

    ttk.Label(frame_city_input, text="City Name:").pack(side=tk.LEFT, padx=5)
    entry_city = ttk.Entry(frame_city_input)
    entry_city.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

    def on_generate_click():
        city = entry_city.get()
        on_submit(city)

    generate_btn = create_button("Generate", on_generate_click, root)

    return entry_city

# statements to call correct weather function
def generate_model(city):
    try:
        weather_data = get_weather(city)
        main_weather = weather_data['weather'][0]['main']

        if main_weather == 'Clear':
            create_sun()
            messagebox.showinfo("Info", "It's warm and sunny! Sun model generated. Exported as Sun.stl")
        elif main_weather in ['Rain', 'Drizzle']:
            create_rain()
            messagebox.showinfo("Info", "It's a terrible day for rain. Rain model generated. Exported as Rain.stl")
        elif main_weather == 'Clouds':
            create_cloud()
            messagebox.showinfo("Info", "Seems cloudy. Cloud model generated. Exported as Cloud.stl")
        elif main_weather == 'Snow':
            create_snow()
            messagebox.showinfo("Info", "Brr, it's snowy! Bring your coat. Snowflake model generated. Exported as Snowflake.stl")
        else:
            messagebox.showinfo("Info", "Weather condition not recognized.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate model: {e}")

# for UI to keep running while the code works with an input
def on_submit(city_name):
    if city_name:
        threading.Thread(target=generate_model, args=(city_name,)).start()
    else:
        messagebox.showerror("Error", "Please enter a city name.")

# Tkinter UI setup, opens a pop-up for the user to type an input. 
root = tk.Tk()
city_entry = enhance_ui(root)  # Call the UI with function
root.mainloop()
