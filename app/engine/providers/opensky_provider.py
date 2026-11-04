from typing import Tuple
from shapely import Point
from pandas import date_range
from datetime import datetime
from shapely import LineString
from ..utils.flight import Flight
from pyopensky.trino import Trino
from collections.abc import Iterator
from geopandas import GeoDataFrame, points_from_xy
from ..utils.validation import type_check, value_check_within, value_check_greater_than


class OpenSkyProvider:
    def __init__(self):
        self.trino = Trino()

    def get(
        self,
        time_start: datetime,
        time_end: datetime,
        bbx: Tuple[float, float, float, float],
    ) -> Iterator[Flight]:
        """
        This function is dedicated to aviation data requesting.

        Args:
            time_start(datetime.datetime): The time from which data is collected
            time_end(datetime.datetime): The time up until which data is collected
            bbx(Tuple[float, float, float, float]): A bounding box determining the area
                for which data is collected. Must be in format:
                [min longitude, min latitude, max longitude, max latitude]

        Returns:
            (GeoDataFrame): Collected data in EPSG:4326 coordinate reference system
        """
        # Sanity check
        type_check(bbx, Tuple, "bbx")
        type_check(time_start, datetime, "time_start")
        type_check(time_end, datetime, "time_end")
        if time_end < time_start:
            raise ValueError("end_time must be later than time_start")
        for i in bbx:
            type_check(i, (float, int), "bounding box coordinate")
        value_check_greater_than(
            obj=bbx[2], val_min=bbx[0], object_name="max_longitude"
        )
        value_check_greater_than(obj=bbx[3], val_min=bbx[1], object_name="max_latitude")
        value_check_within(obj=bbx[0], min=-180, max=180, object_name="min_longitude")
        value_check_within(obj=bbx[2], min=-180, max=180, object_name="max_longitude")
        value_check_within(obj=bbx[1], min=-90, max=90, object_name="min_latitude")
        value_check_within(obj=bbx[3], min=-90, max=90, object_name="max_latitude")

        # Request, prepare and return data
        gdf = self._request_vertices(time_start, time_end, bbx)
        prepared_gdf = self._prepare_vertices(gdf)

        for identifier in prepared_gdf["identifier"].unique():
            flight_vertices = prepared_gdf[prepared_gdf["identifier"] == identifier]
            if len(flight_vertices) > 1:
                yield Flight(
                    callsign=flight_vertices["callsign"].iloc[0],
                    geometry=LineString(flight_vertices.geometry),
                    time_range=(
                        flight_vertices["time"].min(),
                        flight_vertices["time"].max(),
                    ),
                    properties={"icao24": flight_vertices["icao24"].iloc[0]},
                    vertices=flight_vertices,
                )

    def _prepare_vertices(self, gdf):
        cropped_gdf = gdf[["callsign", "icao24", "time", "geometry"]].copy()
        cropped_gdf["identifier"] = cropped_gdf[["callsign", "icao24"]].agg(
            "-".join, axis=1
        )
        return cropped_gdf

    def _request_vertices(self, time_start, time_end, bbx):
        df = self.trino.history(start=time_start, stop=time_end, bounds=bbx)

        if df is None:
            raise Exception("No aviation data collected!")

        # Generate response
        df = df.sort_values("time")
        df = df[df["onground"] == False]
        df = df.dropna(subset=["callsign", "icao24", "lat", "lon", "time"])

        return GeoDataFrame(
            df, geometry=points_from_xy(df.lon, df.lat), crs="EPSG:4326"
        )


if __name__ == "__main__":
    osp = OpenSkyProvider()
    gdf, flights = osp.get(
        time_start=datetime(minute=0, hour=12, day=1, month=12, year=2025),
        time_end=datetime(minute=20, hour=12, day=1, month=12, year=2025),
        bbx=(20.61, 51.82, 21.52, 52.4),
    )
