from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

point = Feature(geometry=Point((33.307643, -111.869107)))
polygon = Polygon(
    [
        [
            (33.305959, -111.876230),
            (33.298606, -111.876230),
            (33.291468, -111.867604),
            (33.294804, -111.859021),
            (33.298714, -111.858935),
            (33.306102, -111.859021),
            (33.305959, -111.867647),
        ]
    ]
)
print(boolean_point_in_polygon(point, polygon))