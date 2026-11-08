from typing import Any
from uuid import uuid4, UUID
from pandas import date_range
from datetime import datetime
from shapely import LineString
from geopandas import GeoDataFrame


class Flight:
    def __init__(
        self,
        callsign: str,
        geometry: LineString,
        time_range: tuple[Any, Any],
        properties: dict,
        vertices: GeoDataFrame,
    ):
        self.id: str = str(uuid4())
        self.callsign: str = callsign
        self.geometry: LineString = geometry
        self.time_range: tuple = time_range
        self.properties: dict = properties
        self.vertices: GeoDataFrame = vertices

    def get_params(self) -> tuple[str, str, tuple[datetime, datetime], LineString, dict]:
        return self.id, self.callsign, self.time_range, self.geometry, self.properties

    def get_vertices(self) -> GeoDataFrame:
        return self.vertices

    def __repr__(self):
        return (
            f"{self.callsign} {self.time_range} "
            f"{', '.join([f'{k}: {v}' for k, v in self.properties.items()])} "
            f"{self.geometry.wkt}"
        )


