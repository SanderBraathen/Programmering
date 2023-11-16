import cadquery as cq

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

create_sun()
print("It's warm and sunny! Exported as Sun.stl")
