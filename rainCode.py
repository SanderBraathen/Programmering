import cadquery as cq

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

create_rain()
print("It's a terrible day for rain. Exported as Rain.stl")

#This code uses scaling, as the file was hard to make initially.


