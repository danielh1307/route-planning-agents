from typing import Optional

from pydantic import BaseModel, Field


class Point(BaseModel):
    lat: float = Field(description="The latitude of the point")
    lng: float = Field(description="The longitude of the point")


class Route(BaseModel):
    distance: float = Field(description="The distance in meters")
    duration: float = Field(description="The time in milliseconds")
    encoded_polyline: str = Field(description="The encoded polyline of the tour")


# class RouteSuggestion(BaseModel):
#     text_from: str = Field(description="a description where the route starts")
#     text_to: str = Field(description="a description where the route ends")
#     website: str = Field(description="a website where more information about the route can be found")
#     description: str = Field(description="a description of the route")
#     start: Optional[Point] = Field(description="the exact start point of the route")
#     end: Optional[Point] = Field(description="the exact end point of the route")


class BoundingBox(BaseModel):
    bottom_left: Point = Field(description="the bottom left point of the bounding box")
    top_right: Point = Field(description="the top right point of the bounding box")


class Region(BaseModel):
    bounding_box: BoundingBox = Field(description="the bounding box defining the region")
    name: str = Field(description="the name of the region")
    display_name: str = Field(description="the display name of the region")
