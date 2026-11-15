import click
from datetime import datetime
from engine.connect.connect_database import DataBaseConnector
from engine.providers.opensky_provider import OpenSkyProvider
from engine.providers.weather_provider import WeatherProvider
from engine.providers.airports_provider import AirportsProvider


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PATH_TO_AIRPORTS = r"/input/airport-codes.csv"


@click.group()
def cli():
    pass


@cli.command()
def get_airports():
    db = DataBaseConnector()
    a = AirportsProvider(PATH_TO_AIRPORTS)
    airports = a.get()
    db.insert_airports(airports)
    click.echo(f"Processed {len(airports)} airports.")


@cli.command()
@click.argument("file")
def get_weather(file: str):
    db = DataBaseConnector()
    wp = WeatherProvider(file)
    metars = wp.get()
    if metars.empty:
        raise click.ClickException("No METARs were decoded from the file.")
    db.insert_metars(metars)
    click.echo(f"Processed {len(metars)} METAR reports.")


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
    
    click.echo(f"Processed {len(flights)} flights.")


if __name__ == "__main__":
    cli()
