# Air-traffic-application
This application is dedicated to acquiring, storing and processing air traffic data.



## How to use it?

```bash
podman compose up --build -d 
```

```bash
podman compose run --rm app python cli.py get-airports
```

```bash
podman compose run --rm app python cli.py get-weather "/input/metars_file.csv"
```

```bash
podman compose run --rm app python cli.py get-flights "2026-11-10 10:00:00" "2026-11-10 10:10:00" 20 51 21 52
```