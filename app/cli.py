# from pyopensky.config import opensky_config_dir

# print(opensky_config_dir, flush=True)

# print("Hello world!", flush=True)

from datetime import datetime
from engine.providers.opensky_provider import OpenSkyProvider

osp = OpenSkyProvider()

for flight in osp.get(
    time_start=datetime(year=2026, month=10, day=2, hour=8),
    time_end=datetime(year=2026, month=10, day=2, hour=8, minute=10),
    bbx=(20.35, 51.7, 21.85, 52.55),
):
    print(flight, flush=True)
