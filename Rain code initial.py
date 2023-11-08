# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:00:17 2023

@author: sande
"""

import cadquery as cq

def create_scaled_cartoon_water_drop(thickness=1.0, scale_factor=3.0):
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

    # Extrude and export the first half
    half_drop = drop_profile.extrude(thickness)
    half_drop.val().exportStl("scaled_half_cartoon_water_drop.stl")

create_scaled_cartoon_water_drop()
