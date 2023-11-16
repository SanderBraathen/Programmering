import cadquery as cq
from math import sin, cos, radians

def create_pentagon_shape():
    # Function to create an extruded pentagon
    def create_pentagon(radius, height, center=(0, 0)):
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
    hole_radius = big_radius * 0.6  # Radius for the larger pentagonal hole

    # Create the central large pentagon
    large_pentagon = create_pentagon(big_radius, height)

    # Cut a larger pentagonal hole in the center of the large pentagon
    pentagon_hole = create_pentagon(hole_radius, height)
    large_pentagon = large_pentagon.cut(pentagon_hole)

    # Initialize a workplane for smaller pentagons
    smaller_pentagons = cq.Workplane("XY")

    # Create and position smaller pentagons
    for i in range(5):
        angle = radians(i * 72)
        x_offset = offset_distance * cos(angle)
        y_offset = offset_distance * sin(angle)
        smaller_pentagon = create_pentagon(small_radius, height, center=(x_offset, y_offset))
        smaller_pentagons = smaller_pentagons.union(smaller_pentagon)

    # Combine the large pentagon with the smaller ones
    combined_shape = large_pentagon.union(smaller_pentagons)

    # Get the solid and scale it by 4 times
    scaled_shape = combined_shape.val().scale(4)

    # Export the STL file
    cq.exporters.export(scaled_shape, "scaled_pentagon_shape.stl")

create_pentagon_shape()
print("Scaled pentagon shape with a pentagon hole created and exported as scaled_pentagon_shape.stl")

