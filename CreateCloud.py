# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 18:23:39 2023

@author: sande
"""

import cadquery as cq

def create_compact_cloud():
    # Central ellipsoid to serve as the main body of the cloud
    cloud = cq.Workplane("XY").ellipse(4, 6).extrude(1)

    # Manually defined arrangement of ellipsoids to form the cloud shape, with two removed
    cloud_points = [
        (-5, 1, 0), (6, -2, 0),  # Varied positions for a more natural look
        (0, -6, 0), (7, 3, 0), (-6, -3, 0),
        (3, -5, 0),  (1, 1, 0)
    ]
    ellipsoid_sizes = [
        (2.5, 2), (2.8, 3), (4, 3.5), (3.5, 4), (2.7, 3), 
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

    # Export the compact cloud as an STL file
    cloud.val().exportStl("compact_cloud.stl")

create_compact_cloud()
