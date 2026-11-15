import pandas as pd
from pathlib import Path
from geopandas import GeoDataFrame, points_from_xy


class AirportsProvider:
    def __init__(self, path: str):
        self.path_to_file: Path = Path(path)

    def get(self) -> GeoDataFrame:
        """
        This function reads .csv file with airports' code
        and returns a GeoDataFrame with that data.

        Returns:
            (GeoDataFrame): File with goems
        """
        df = pd.read_csv(
            self.path_to_file,
            delimiter=",",
            usecols=["icao_code", "gps_code", "coordinates"],
        )

        df["icao_code"] = df["icao_code"].fillna(df["gps_code"])
        df = df.dropna(subset=["icao_code", "coordinates"]).drop_duplicates("icao_code")
        df[["lat", "lon"]] = (
            df["coordinates"].str.split(", ", n=1, expand=True).astype(float)
        )

        return GeoDataFrame(
            df["icao_code"],
            geometry=points_from_xy(df["lon"], df["lat"]),
            crs="EPSG:4326",
        )
