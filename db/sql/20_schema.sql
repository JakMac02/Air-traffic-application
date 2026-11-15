CREATE EXTENSION IF NOT EXISTS postgis;


CREATE TABLE flight(
    id UUID PRIMARY KEY,
    callsign TEXT NOT NULL,
    time_start TIMESTAMPTZ,
    time_end TIMESTAMPTZ,
    geometry geometry(LINESTRING,4326) NOT NULL
);

CREATE TABLE vertex(
    id SERIAL PRIMARY KEY,
    time timestamp without time zone NOT NULL,
    baroaltitude REAL,
    alert BOOL,
    heading REAL,
    velocity REAL,
    vertrate REAL,
    geometry geometry(POINT,4326) NOT NULL,
    flight_id UUID,
    FOREIGN KEY(flight_id)
       REFERENCES flight(id)
       ON DELETE CASCADE
);


CREATE TABLE meteo_station(
    id SERIAL PRIMARY KEY,
    icao_code CHAR(4) NOT NULL UNIQUE,
    geometry geometry(POINT, 4326) NOT NULL
);


CREATE TABLE weather(
    id SERIAL PRIMARY KEY,
    icao_code CHAR(4) NOT NULL REFERENCES meteo_station (icao_code),
    time TIMESTAMPTZ NOT NULL,
    temperature REAL,
    dew_point REAL,
    wind_speed REAL,
    wind_dir REAL,
    wind_gust REAL,
    visibility REAL,
    pressure REAL,
    description TEXT,
    cloud_base REAL,
    snow_depth REAL,
    precipitation1h REAL,
    precipitation3h REAL,
    precipitation6h REAL,
    precipitation24h REAL,
    raw_metar TEXT NOT NULL,
    UNIQUE (icao_code, time)
);


CREATE INDEX flight_geometry_idx ON flight USING GIST (geometry);
CREATE INDEX flight_callsign_idx ON flight(callsign);
CREATE INDEX vertex_geometry_idx ON vertex USING GIST (geometry);
CREATE INDEX vertex_time_idx ON vertex(time);
CREATE INDEX meteo_station_point_idx ON meteo_station USING gist (geom);
