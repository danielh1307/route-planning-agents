import os

import requests
from langchain_core.tools import tool

from src.route.models import Point, Route, BoundingBox, Region


# def get_node(id: str) -> Point:
#     data_param = f"[out:json];node({id});out body;"
#     url = "https://overpass-api.de/api/interpreter"
#     params = {
#         "data": data_param
#     }
#
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#
#     data = response.json()
#
#     if "elements" not in data or len(data["elements"]) == 0:
#         print("No elements found in response for id ", id)
#         return None
#
#     return Point(lat=data["elements"][0]["lat"], lng=data["elements"][0]["lon"])


@tool
def get_detailed_route(start_point: Point, end_point: Point, vehicle: str) -> Route:
    """This function takes three arguments, a start point, an end point and a vehicle.
    The vehicle is either 'bike', 'foot' or 'car'.
    It returns an exact route between these two points.
    Call this function whenever you want to have a detailed route."""
    url = (f"https://graphhopper.com/api/1/route?point={start_point.lat},{start_point.lng}"
           f"&point={end_point.lat},{end_point.lng}&vehicle={vehicle}&key={os.environ['GRAPHHOPPER_API_KEY']}")
    print(url)
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    if "paths" not in data:
        raise Exception("No paths found in response")

    path = data["paths"][0]
    return Route(distance=path["distance"], duration=path["time"], encoded_polyline=path["points"])


# @tool
# def get_route_suggestions(bounding_box: BoundingBox, vehicle: str) -> list[RouteSuggestion]:
#     """To a specific bounding box and a vehicle type, we get multiple route suggestions.
#     Use one of the following for input parameter vehicle: hiking, foot, bicycle.
#     """
#
#     # filter by length: https://chatgpt.com/c/671d46e2-1254-8011-a76c-879f46e76858
#     # alternativ könnte ich auch einfach start bis ende Punkt rechnen aber das
#     # wäre dann wohl Luftlinie
#     # out geom erspart mit wohl den 2. Call weil die Geometrie schon mitkommt
#
#     # different vehicle are possible like:
#     # hiking, foot
#     # bicycle, mtb
#     max_suggestions = 10
#
#     data_param = f"[out:json];(relation['route'='{vehicle}']({bounding_box.bottom_left.lat},{bounding_box.bottom_left.lng},{bounding_box.top_right.lat},{bounding_box.top_right.lng}););out body;"
#     url = "https://overpass-api.de/api/interpreter"
#     params = {
#         "data": data_param
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#
#     data = response.json()
#
#     if "elements" not in data:
#         raise Exception("No elements found in response")
#
#     suggestions = []
#     if (len(data['elements'])) > max_suggestions:
#         print(f"We have found {len(data['elements'])} possible routes but we return only {max_suggestions}")
#
#     for element in data["elements"]:
#         start_point = get_node(element["members"][0]["ref"])
#         end_point = get_node(element["members"][-1]["ref"])
#
#         if start_point is None or end_point is None:
#             continue
#
#         suggested_route = {
#             "text_from": element["tags"].get("from", ""),
#             "text_to": element["tags"].get("to", ""),
#             "website": element["tags"].get("website", ""),  # might not exist
#             "description": element["tags"].get("description", ""),  # might not exist
#             "start": start_point,
#             "end": end_point
#         }
#         suggestions.append(RouteSuggestion(**suggested_route))
#
#         if len(suggestions) == max_suggestions:
#             break
#
#     return suggestions


@tool
def get_coordinates(region: str) -> list[Region]:
    """To a given city or region name, we get a list of Region objects, specifying
    the exact bounding box and name of that region
    """

    url = f"https://nominatim.openstreetmap.org/search?q={region}&format=json"

    headers = {
        "User-Agent": "Agent/1.0 (hamm.daniel@gmail.com)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    print(data)

    regions = []

    for d in data:
        bottom_left_point = Point(lat=float(d["boundingbox"][0]), lng=float(d["boundingbox"][2]))
        top_right_point = Point(lat=float(d["boundingbox"][1]), lng=float(d["boundingbox"][3]))
        bounding_box = BoundingBox(bottom_left=bottom_left_point, top_right=top_right_point)
        print(bounding_box)

        region = {
            "bounding_box": bounding_box,
            "name": d["name"],
            "display_name": d["display_name"]
        }

        regions.append(Region(**region))

    return regions
