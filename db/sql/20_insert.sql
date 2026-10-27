CREATE EXTENSION IF NOT EXISTS postgis;


CREATE TABLE flight(
    id SERIAL PRIMARY KEY,
    callsign TEXT NOT NULL,
    icao24 TEXT,
    geometry geometry(LINESTRINGZ,4326) NOT NULL
);

CREATE TABLE vertex(
    id SERIAL PRIMARY KEY,
    time timestamp without time zone NOT NULL,
    onground BOOL,
    alert BOOL,
    heading REAL,
    velocity REAL,
    vertrate REAL,
    geometry geometry(POINT,4326) NOT NULL,
    flight_id INT,
    FOREIGN KEY(flight_id)
       REFERENCES flight(id)
       ON DELETE CASCADE
);


CREATE INDEX flight_geometry_idx ON flight USING GIST (geometry);
CREATE INDEX flight_callsign_idx ON flight(callsign);
CREATE INDEX vertex_geometry_idx ON vertex USING GIST (geometry);
CREATE INDEX vertex_time_idx ON vertex(time);
