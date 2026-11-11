import click
from datetime import datetime
from engine.connect.connect_database import DataBaseConnector
from engine.providers.opensky_provider import OpenSkyProvider

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@click.group()
def cli():
    pass


@cli.command()
@click.argument("start")
@click.argument("stop")
@click.argument("bbx", nargs=4, type=float)
def get_flights(start: str, stop: str, bbx: tuple[float, float, float, float]):
    time_start = datetime.strptime(start, DATETIME_FORMAT)
    time_stop = datetime.strptime(stop, DATETIME_FORMAT)
    osp = OpenSkyProvider()
    db = DataBaseConnector()

    flights = [
        flight
        for flight in osp.get(
            time_start=time_start,
            time_end=time_stop,
            bbx=bbx,
        )
    ]

    db.insert_flights(flights)


if __name__ == "__main__":
    cli()
