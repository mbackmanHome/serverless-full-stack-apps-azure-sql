import logging
import json
import turfpy
from datetime import datetime, timezone
from typing import Any

import requests
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature



def get_timestamp(timestamp: str) -> str:
    """return the timestamp in a human readable string"""
    return datetime.fromtimestamp(int(timestamp), timezone.utc).isoformat(sep=' ')

def get_bus_data_from_feed(feed_url:str) -> list[dict[str, Any]]:
    """Retrieve the raw bus data from the GTFS Real Time Feed"""
    response = requests.get(feed_url)
    response.raise_for_status() # raise exception if not 200
    return response.json()


def get_monitored_format(record: dict) -> dict:
    """Create a custom dictionary from a passed record information"""

    return dict(
        DirectionId=record['trip']['directionId'],
        RouteId=record['trip']['routeId'],
        VehicleId=record['vehicle']['id'], # full path from file is ['vehicle']['vehicle']['id']
        Position={
            "Latitude": record['position']['latitude'],
            "Longitude": record['position']['longitude']
        },
        
        TimestampUTC= get_timestamp(record['timestamp'])
    )


def get_route_id(bus_data: dict) -> str:
    """Return the route_id from the monitored_route"""
    return bus_data["vehicle"]["trip"]["routeId"]


def get_geo_fences2(conn) -> list:
    with conn.cursor() as cursor:
        cursor.execute("EXEC web.GetGeoFence")

        #result = list()

        result = cursor.fetchone()[0]

        result2 =  result.split(';')

        #result3 = [str(i) for i in result2]

        results3 = list()
        for y in result2:
            z = y.split(',')
            x = [float(i) for i in z]

            results3.append(tuple(x))

        return results3

def get_geo_fences(conn, payload: list[dict[str: Any]]):
    """Connect to the SQL Database and execute the passed procedure"""
    with conn.cursor() as cursor:
        result={}
        logging.info(f"passing {payload=}")
        cursor.execute(f"EXEC web.AddBusData ?", json.dumps(payload))
        result = cursor.fetchone()[0]

        if result:
            result = json.loads(result) 
        else:
            result = {} ##[{'BusDataId': 6267, 'VehicleId': 7417, 'DirectionId': 1, 'RouteId': 100113, 'RouteName': '221', 'GeoFenceId': 12, 'GeoFence': 'Crossroads', 'GeoFenceStatus': 'Enter', 'TimestampUTC': '2022-09-06T21:24:07'}]


    return result 

def get_monitored_routes(conn) -> list[int]:
    """Return a list of the route_ids to inspect for"""
    with conn.cursor() as cursor:
        cursor.execute(f"EXEC web.GetMonitoredRoutes")
        results = json.loads(cursor.fetchone()[0])
        routes = [str(route['route_id']) for route in results]
    return routes
 

def trigger_logic_app(fence, logic_app_url: str) -> None:
        content = {
            "VehicleId": str(fence["VehicleId"]), 
            "RouteId": str(fence["RouteId"]),
            "TimestampUTC": str(fence["TimestampUTC"])
        }

        logging.info("Calling Logic App webhook for {0}".format(fence["VehicleId"]))
        print("Calling Logic App webhook for {0}".format(fence["VehicleId"]))

        params = { 
            "Content-type": "application/json" 
        }

        response = requests.post(logic_app_url, json=content, headers=params)
        response.raise_for_status()
        return response
        


def get_geo_fence_status(latitude: float, longitude: float, geofence: list[tuple]) -> bool:
    point = Feature(geometry=Point((latitude, longitude)))
    polygon = Polygon([geofence])
    
    return boolean_point_in_polygon(point, polygon)

