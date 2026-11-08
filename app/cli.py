from datetime import datetime
from engine.connect.connect_database import DataBaseConnector
from engine.providers.opensky_provider import OpenSkyProvider

osp = OpenSkyProvider()
db = DataBaseConnector()

flights = [
    flight
    for flight in osp.get(
        time_start=datetime(year=2026, month=10, day=2, hour=8),
        time_end=datetime(year=2026, month=10, day=2, hour=8, minute=10),
        bbx=(20.35, 51.7, 21.85, 52.55),
    )
]

db.insert_flights(flights)
