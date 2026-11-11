from typing import Any
from uuid import uuid4, UUID
from datetime import datetime
from shapely import LineString
from pandas import DatetimeIndex
from geopandas import GeoDataFrame


class Flight:
    def __init__(
        self,
        callsign: str,
        geometry: LineString,
        time_start: datetime,
        time_end: datetime,
        properties: dict,
        vertices: GeoDataFrame,
    ):
        self.id: str = str(uuid4())
        self.callsign: str = callsign
        self.geometry: LineString = geometry
        self.time_start: datetime = time_start
        self.time_end: datetime = time_end
        self.properties: dict = properties
        # vertices["Address"] = self.id
        self.vertices: GeoDataFrame = vertices

    def get_params(
        self,
    ) -> tuple[str, str, datetime, datetime, LineString, dict]:
        return (
            self.id,
            self.callsign,
            self.time_start,
            self.time_end,
            self.geometry,
            self.properties,
        )

    def get_vertices(self) -> GeoDataFrame:
        return self.vertices

    def __repr__(self):
        return (
            f"{self.callsign} {self.time_start} {self.time_end}"
            f"{', '.join([f'{k}: {v}' for k, v in self.properties.items()])} "
            f"{self.geometry.wkt}"
        )
