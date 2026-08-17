#!C:\Users\Даниил\AppData\Local\Python\bin\python.exe

import html
import json
import io
import sys
import traceback
from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CACHE_FILE = Path(r"C:\xampp\FCC-Musberg\flight_cache.json")
CONFIG_FILE = Path(r"C:\xampp\FCC-Musberg\environment.cfg")
AIRPORT_CODE = "STR"

API_URL = (
    "https://aerodatabox.p.rapidapi.com"
    f"/flights/airports/iata/{AIRPORT_CODE}"
)


def output_headers(content_type="text/html; charset=utf-8"):
    print(f"Content-Type: {content_type}")
    print("Cache-Control: no-store")
    print()
    
def is_cache_valid():
    """Проверка: не устарел ли кэш (менее 1 часа)."""
    if not CACHE_FILE.exists():
        return False
    try:
        with open(CACHE_FILE, 'r', encoding="utf-8") as f:
            cache_data = json.load(f)
        cache_time = datetime.fromisoformat(cache_data["timestamp"])
        return (datetime.now(ZoneInfo("Europe/Berlin")) - cache_time) < timedelta(hours=1)
    except Exception:
        return False

def read_cache():
    """Чтение данных из кэша."""
    with open(CACHE_FILE, 'r', encoding="utf-8") as f:
        return json.load(f)["data"]
    
def read_cache_timestamp():
    """Чтение timestamp из кэша."""
    with open(CACHE_FILE, 'r') as f:
        return json.load(f)["timestamp"]

def write_cache(data):
    """Запись данных в кэш с временной меткой."""
    cache_entry = {
        "timestamp": datetime.now(ZoneInfo("Europe/Berlin")).isoformat(),
        "data": data
    }
    with open(CACHE_FILE, 'w', encoding="utf-8") as f:
        json.dump(cache_entry, f)

def load_api_key():
    config = ConfigParser()

    loaded_files = config.read(
        CONFIG_FILE,
        encoding="utf-8"
    )

    if not loaded_files:
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    if not config.has_section("aerodatabox"):
        raise KeyError(
            "Section [aerodatabox] is missing in environment.cfg"
        )

    if not config.has_option("aerodatabox", "rapidapi_key"):
        raise KeyError(
            "Property rapidapi_key is missing in "
            "section [aerodatabox]"
        )

    api_key = config.get(
        "aerodatabox",
        "rapidapi_key"
    ).strip()

    if not api_key:
        raise ValueError("The AeroDataBox API key is empty")

    return api_key


def get_stuttgart_flights(api_key):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
        "Accept": "application/json"
    }

    params = {
        # Start 30 minutes before the current time.
        "offsetMinutes": -30,

        # Return a total window of 90 minutes:
        # 30 minutes before now and 60 minutes after now.
        "durationMinutes": 60,

        # Return both arrivals and departures.
        "direction": "Both",

        # Include the opposite airport for each flight.
        "withLeg": "true",

        # Avoid duplicate flights caused by codeshares.
        "withCodeshared": "false",

        "withCancelled": "true",
        "withCargo": "false",
        "withPrivate": "false",
        "withLocation": "false"
    }

    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    if not response.ok:
        raise RuntimeError(
            f"AeroDataBox returned HTTP {response.status_code}: "
            f"{response.text[:1000]}"
        )

    return response.json()


def get_airport_name(flight_section):
    airport = flight_section.get("airport") or {}

    airport_name = airport.get("name") or "Unknown airport"
    airport_iata = airport.get("iata")
    airport_icao = airport.get("icao")

    airport_code = airport_iata or airport_icao or ""

    if airport_code:
        return f"{airport_name} ({airport_code})"

    return airport_name


def get_flight_number(flight):
    return (
        flight.get("number")
        or flight.get("callSign")
        or "Unknown"
    )


def get_airline_name(flight):
    airline = flight.get("airline") or {}
    return airline.get("name") or "Unknown airline"


def get_time(section):
    movement_times = [
        section.get("revisedTime"),
        section.get("predictedTime"),
        section.get("scheduledTime"),
        section.get("runwayTime")
    ]

    for movement_time in movement_times:
        if movement_time and movement_time.get("local"):
            return movement_time["local"]

    return ""


def format_time(value):
    if not value:
        return "—"

    try:
        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        return parsed.strftime("%H:%M")
    except ValueError:
        return value


def escape(value):
    return html.escape(str(value or ""))


def create_flight_rows(flights, direction):
    rows = []

    for flight in flights:
        flight_number = get_flight_number(flight)
        airline = get_airline_name(flight)
        status = flight.get("status") or "Unknown"

        departure = flight.get("departure") or {}
        arrival = flight.get("arrival") or {}

        if direction == "arrival":
            airport = get_airport_name(departure)
            movement_time = get_time(arrival)
        else:
            airport = get_airport_name(arrival)
            movement_time = get_time(departure)

        rows.append(
            "<tr>"
            f"<td>{escape(format_time(movement_time))}</td>"
            f"<td>{escape(flight_number)}</td>"
            f"<td>{escape(airline)}</td>"
            f"<td>{escape(airport)}</td>"
            f"<td>{escape(status)}</td>"
            "</tr>"
        )

    if not rows:
        return (
            '<tr><td colspan="5">'
            "No flights found in this time window."
            "</td></tr>"
        )

    return "\n".join(rows)


def render_page(data, generated_at):
    arrivals = data.get("arrivals") or []
    departures = data.get("departures") or []

    updated_time = generated_at[0:19].replace("T", " ")

    arrival_rows = create_flight_rows(
        arrivals,
        "arrival"
    )

    departure_rows = create_flight_rows(
        departures,
        "departure"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="60">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>Stuttgart Airport Flights</title>

    <style>
        body {{
            margin: 0;
            padding: 24px;
            background: #f4f6f8;
            color: #1f2937;
            font-family: Arial, Helvetica, sans-serif;
        }}

        main {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        h1 {{
            margin-bottom: 6px;
        }}

        h2 {{
            margin-top: 32px;
        }}

        .updated {{
            margin-bottom: 24px;
            color: #6b7280;
        }}

        .summary {{
            display: flex;
            gap: 16px;
            margin: 20px 0;
        }}

        .summary div {{
            padding: 16px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        }}

        .table-container {{
            overflow-x: auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th,
        td {{
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
            text-align: left;
        }}

        th {{
            background: #1f2937;
            color: white;
        }}

        tr:hover {{
            background: #f9fafb;
        }}

        .note {{
            margin-top: 24px;
            color: #6b7280;
            font-size: 0.9rem;
        }}
    </style>
</head>

<body>
<main>
    <h1>Stuttgart Airport</h1>

    <div class="updated">
        Airport: STR / EDDS - Updated: {escape(updated_time)}
    </div>

    <div class="summary">
        <div>
            <strong>{len(arrivals)}</strong><br>
            arrivals
        </div>

        <div>
            <strong>{len(departures)}</strong><br>
            departures
        </div>
    </div>

    <h2>Arrivals at Stuttgart</h2>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Flight</th>
                    <th>Airline</th>
                    <th>Origin</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {arrival_rows}
            </tbody>
        </table>
    </div>

    <h2>Departures from Stuttgart</h2>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Flight</th>
                    <th>Airline</th>
                    <th>Destination</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {departure_rows}
            </tbody>
        </table>
    </div>

    <p class="note">
        Time window: 30 minutes before refresh through
        30 minutes after refresh. The page refreshes every hour.
    </p>
</main>
</body>
</html>"""


def main():
    try:
        if is_cache_valid():
            flight_data = read_cache()
        else:
            api_key = load_api_key()
            flight_data = get_stuttgart_flights(api_key)
            write_cache(flight_data)


        output_headers()
        print(render_page(flight_data, read_cache_timestamp()))

    except Exception as error:
        output_headers()

        print("<!DOCTYPE html>")
        print("<html><head><meta charset='utf-8'>")
        print("<title>Flight API error</title></head><body>")
        print("<h1>Flight API error</h1>")
        print(f"<p>{escape(error)}</p>")

        # Local troubleshooting only.
        print("<pre>")
        print(escape(traceback.format_exc()))
        print("</pre>")

        print("</body></html>")


if __name__ == "__main__":
    main()