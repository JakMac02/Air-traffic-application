import os
from pandas import concat
from ..utils.flight import Flight
from geopandas import GeoDataFrame
from sqlalchemy import create_engine, URL


POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]


class DataBaseConnector:
    def __init__(self):
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.db = POSTGRES_DB
        self.host = POSTGRES_HOST

    def _db_url(self):
        return URL.create(
            "postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
        )

    def _engine(self):
        return create_engine(self._db_url())

    def insert_flights(self, flights: list[Flight]):
        engine = self._engine()

        ids, callsings, geometries, time_ranges, vertices = [], [], [], [], []    

        for f in flights:
            i, call, t, geom, p = f.get_params()
            ids.append(i)
            callsings.append(call)
            geometries.append(geom)
            time_ranges.append(t)
            v = f.vertices
            v["flight_id"] = i
            vertices.append(v)

        flights_gdf = GeoDataFrame(
            {
                "id": ids,
                "callsign": callsings,
                "time_range": time_ranges, 
            },
            geometry=geometries,
            crs=4326,
        )

        vertices_gdf = GeoDataFrame(concat(vertices), crs=4326)

        flights_gdf.to_postgis("flight", engine, if_exists="append", index=False)
        vertices_gdf.to_postgis("vertex", engine, if_exists="append", index=False)
        
    

