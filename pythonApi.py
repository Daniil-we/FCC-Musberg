from pyopensky.rest import REST
import os
from pathlib import Path
import configparser
from datetime import datetime, timedelta, timezone

PROJECT_ROOT = Path(__file__).resolve().parent
config_file = PROJECT_ROOT / "environment.cfg"
cfg = configparser.ConfigParser()
cfg.read(config_file)
os.environ["OPENSKY_CLIENT_ID"] = cfg["oauth"]["CLIENT_ID"]
os.environ["OPENSKY_CLIENT_SECRET"] = cfg["oauth"]["CLIENT_SECRET"]
rest = REST()
end = datetime.now(timezone.utc)
begin = end - timedelta(hours=12)
arrivals = rest.arrival(airport="EDDS", begin=begin, end=end)

print(arrivals)
print("Number of arrivals:", len(arrivals))