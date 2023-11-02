import cadquery as cq

def create_sun():
    core_height = 1  # Core height
    sun_core = cq.Workplane("XY").circle(5).extrude(core_height)  # Flat, round core
    x_length = 3.5
    y_length = 0.5

    # Create rays
    for angle in range(0, 360, 45):
        ray_profile = (
            cq.Workplane("XY")
            .center(5, 0)
            .ellipse(x_length, y_length)
            .extrude(core_height)
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        sun_core = sun_core.union(ray_profile)

    # To scale the model, you need to apply a scaling transformation
    scale_factor = 2  # The uniform scaling factor for all directions
    scaled_sun = sun_core.val().scale(scale_factor)

    # Export the STL file
    scaled_sun.exportStl("sun.stl")

create_sun()
print("Scaled-up sun model has been created and exported as sun.stl")