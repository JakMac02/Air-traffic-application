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
            "postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
        )

    def _engine(self):
        return create_engine(self._db_url())

    def insert_flights(self, flights: list[Flight]):
        engine = self._engine()

        flights_gdf, vertices_gdf = self._flights_to_gdfs(flights)
        flights_gdf.to_postgis("flight", engine, if_exists="append", index=False)
        vertices_gdf.to_postgis("vertex", engine, if_exists="append", index=False)

    def _flights_to_gdfs(
        self, flights: list[Flight]
    ) -> tuple[GeoDataFrame, GeoDataFrame]:
        ids, callsings, geometries, time_starts, time_ends, vertices = (
            [],
            [],
            [],
            [],
            [],
            [],
        )

        for f in flights:
            print(f)
            i, call, t_start, t_end, geom, p = f.get_params()
            ids.append(i)
            callsings.append(call)
            geometries.append(geom)
            time_starts.append(t_start)
            time_ends.append(t_end)
            v = f.vertices
            v["flight_id"] = i
            vertices.append(v)
            print(v.columns, flush=True)

        return (
            GeoDataFrame(
                {
                    "id": ids,
                    "callsign": callsings,
                    "time_start": time_starts,
                    "time_end": time_ends,
                },
                geometry=geometries,
                crs=4326,
            ),
            GeoDataFrame(concat(vertices), crs=4326),
        )
