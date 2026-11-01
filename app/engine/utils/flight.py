from typing import Any
from pandas import date_range
from datetime import datetime
from shapely import LineString
from geopandas import GeoDataFrame


class Flight:
    def __init__(self, callsign: str, geometry: LineString, time_range: tuple[Any, Any], properties: dict, vertices: GeoDataFrame):
        self.callsign = callsign
        self.geometry = geometry
        self.time_range = time_range
        self.properties = properties
        self.vertices = vertices


    def get_params(self) -> tuple[str, tuple[datetime, datetime], LineString, dict]:
        return self.callsign, self.time_range, self.geometry, self.properties


    def get_vertices(self) -> GeoDataFrame:
        return self.vertices