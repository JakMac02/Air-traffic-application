import csv
from metar import Metar
from pathlib import Path
from pandas import DataFrame
from datetime import datetime, timezone


class WeatherProvider:
    def __init__(self, path: str):
        self.path_to_file: Path = Path(path)

    def get(self) -> DataFrame:

        rows = []

        with open(self.path_to_file, "r") as f:
            delimiter = "\t" if "\t" in f.readline() else ","
            f.seek(0)
            reader_obj = csv.reader(f, delimiter=delimiter)
            for row in reader_obj:
                try:
                    dt = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=timezone.utc
                    )

                    decoded = Metar.Metar(row[3], dt.month, dt.year)
                    heights = [height.value("M") for cover, height, cloud in decoded.sky if height is not None]
                    rows.append(
                        {
                            "icao_code": row[1],
                            "time": dt,
                            "temperature": decoded.temp.value("C") if decoded.temp else None,
                            "dew_point": decoded.dewpt.value("C") if decoded.dewpt else None,
                            "wind_speed": decoded.wind_speed.value("KT") if decoded.wind_speed else None,
                            "wind_dir": decoded.wind_dir.value() if decoded.wind_dir else None,
                            "wind_gust": decoded.wind_gust.value("KT") if decoded.wind_gust else None,
                            "visibility": decoded.vis.value("M") if decoded.vis else None,
                            "pressure": decoded.press.value("HPA") if decoded.press else None,
                            "description": decoded.present_weather() or None,
                            "cloud_base": min(heights, default=None),
                            "snow_depth": decoded.snowdepth.value("M") * 100 if decoded.snowdepth else None,
                            "precipitation1h": decoded.precip_1hr.value("CM") if decoded.precip_1hr else None,
                            "precipitation3h": decoded.precip_3hr.value("CM") if decoded.precip_3hr else None,
                            "precipitation6h": decoded.precip_6hr.value("CM") if decoded.precip_6hr else None,
                            "precipitation24h": decoded.precip_24hr.value("CM") if decoded.precip_24hr else None,
                            "raw_metar": row[3],
                        }
                    )
                
                except Exception as e:
                    print("Error during decoding Metar row:", e, flush=True)

        return DataFrame(rows)