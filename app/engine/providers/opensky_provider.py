from typing import Tuple
from shapely import Point
from datetime import datetime
from pyopensky.trino import Trino
from geopandas import GeoDataFrame, points_from_xy


class OpenSkyProvider:
    def __init__(self):
        self.trino = Trino()

    def get(
        self,
        time_start: datetime,
        time_end: datetime,
        bbx: Tuple[float, float, float, float],
    ):
        """
        This function is dedicated to aviation data requesting.

        Args:
            time_start(datetime.datetime): The time from which data is collected
            time_end(datetime.datetime): The time up until which data is collected
            bbx(Tuple[float, float, float, float]): A bounding box determining the area
                for which data is collected. Must be in format:
                `[min_longitude, min_latitude, max_longitude, max_latitude]'

        Returns:
            (GeoDataFrame): Collected data in EPSG:4326 coordinate reference system
        """
        # Sanity check
        if not isinstance(time_start, datetime):
            raise TypeError(
                f"time_start is of type {type(time_start)}. Should be datetime.datetime"
            )
        if not isinstance(time_end, datetime):
            raise TypeError(
                f"time_end is of type {type(time_end)}. Should be datetime.datetime"
            )
        if time_end < time_start:
            raise ValueError("end_time must be later than time_start")
        if not isinstance(bbx, Tuple):
            raise TypeError("Provided bounding box must be of a type Tuple")
        for i in bbx:
            if not isinstance(i, (float, int)):
                raise TypeError(
                    f"Bounding box coordinates must be of a type float not {type(i)}"
                )
        if bbx[2] < bbx[0]:
            raise ValueError(
                "A bounding box must be in format: "
                "[min_longitude, min_latitude, max_longitude, max_latitude] "
                f"min_longitude = {bbx[0]} can't be greater than max_longitude = {bbx[2]}"
            )
        if bbx[3] < bbx[1]:
            raise ValueError(
                "A bounding box must be in format: "
                "[min_longitude, min_latitude, max_longitude, max_latitude] "
                f"min_latitude = {bbx[1]} can't be greater than max_latitude = {bbx[3]}"
            )
        if -180 > bbx[0] or 180 < bbx[0]:
            raise ValueError(
                f"min_longitude must be in range <-180, 180> and can't be {bbx[0]}"
            )
        if -180 > bbx[2] or 180 < bbx[2]:
            raise ValueError(
                f"max_longitude must be in range <-180, 180> and can't be {bbx[2]}"
            )
        if -90 > bbx[1] or bbx[1] > 90:
            raise ValueError(
                f"min_latitude must be in range <-90, 90> and can't be {bbx[0]}"
            )
        if -90 > bbx[3] or bbx[3] > 90:
            raise ValueError(
                f"max_latitude must be in range <-90, 90> and can't be {bbx[3]}"
            )

        # Request data
        df = self.trino.history(start=time_start, stop=time_end, bounds=bbx)

        if df is None:
            raise Exception("No aviation data collected!")

        # Generate response
        return GeoDataFrame(
            df, geometry=points_from_xy(df.lon, df.lat), crs="EPSG:4326"
        )


if __name__ == "__main__":
    osp = OpenSkyProvider()
    gdf = osp.get(
        time_start=datetime(minute=0, hour=12, day=1, month=12, year=2025),
        time_end=datetime(minute=20, hour=12, day=1, month=12, year=2025),
        bbx=(20.61, 51.82, 21.52, 52.4),
    )
    print(gdf.head())
