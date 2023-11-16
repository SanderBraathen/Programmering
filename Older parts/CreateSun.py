import cadquery as cq

def create_sun():
    core_height = 1 * 4  # Core height, scaled by 2x
    sun_core = cq.Workplane("XY").circle(5 * 4).extrude(core_height)  # Scale radius by 4x and height by 2x

    x_length = 3.5 * 8  # Scale by 4x
    y_length = 0.5 * 8  # Scale by 4x

    # Create rays with scaled dimensions
    for angle in range(0, 360, 45):
        ray_profile = (
            cq.Workplane("XY")
            .center(5 * 4, 0)  # Position scaled by 4x
            .ellipse(x_length, y_length)
            .extrude(core_height)  # Extrude thickness scaled by 2x
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        sun_core = sun_core.union(ray_profile)

    # Export the STL file
    cq.exporters.export(sun_core, "sun.stl")

create_sun()
print("Scaled-up sun model has been created and exported as sun.stl")
