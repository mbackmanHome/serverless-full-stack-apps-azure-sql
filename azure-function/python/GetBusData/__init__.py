import logging
import os
from typing import Any

import azure.functions as func
import pyodbc
import json
import requests

from datetime import datetime
from .bus_data_process import (
    get_bus_data_from_feed,
    get_geo_fences,
    get_geo_fences2,
    get_monitored_format,
    get_monitored_routes,
    get_route_id,
    trigger_logic_app,
    get_geo_fence_status
)

AZURE_CONN_STRING: str = os.environ["AzureSQLConnectionString"]
GTFS_REAL_TIME_FEED: str = os.environ["RealTimeFeedUrl"]
LOGIC_APP_URL: str = os.environ.get("LogicAppUrl", "")


def main(GetBusData: func.TimerRequest) -> None:
    """Retrieve the routes we want to monitor from the SQL Database"""
    conn: str = pyodbc.connect(AZURE_CONN_STRING)

    logging.info(f"Executed Successfully!")


    monitored_routes: list[int] = get_monitored_routes(conn)
    logging.info(f"{len(monitored_routes)} routes to check against")
    entities = get_bus_data_from_feed(GTFS_REAL_TIME_FEED)['entity']
    logging.info(monitored_routes)
    #logging.info(entities)
    #print(entities)
    entities2 = [i for i in entities if i['vehicle'].get('trip') is not None]

    # reformat the bus_feed to match the format of the monitored_routes
    monitored_buses = [get_monitored_format(bus['vehicle']) for bus in entities2 if get_route_id(bus) in monitored_routes]
    logging.info(f"{len(entities2)} buses found. {len(monitored_buses)} buses monitored.")
    

    print(monitored_buses)

    
    if not monitored_buses:
        logging.info("No Monitored Bus Routes Detected")
        return

    out = get_geo_fences2(conn)

   
    for bus in monitored_buses:
        print(bus['VehicleId'] )
        lat = bus['Position']['Latitude']
        long = bus['Position']['Longitude']

        geo_fence_status = get_geo_fence_status(lat, long, out)

        if geo_fence_status:
            print("yes!")
            fence_success = {"TimestampUTC": str(bus['TimestampUTC']),
                "RouteId": str(bus['RouteId']),
                "VehicleId": str(bus['VehicleId'])
                }
        
            trigger_logic_app(fence_success, LOGIC_APP_URL)