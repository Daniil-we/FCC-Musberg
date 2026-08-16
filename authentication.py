import configparser
from pathlib import Path
import requests
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
config = configparser.ConfigParser()
PROJECT_ROOT = Path(__file__).resolve().parent
config_file = PROJECT_ROOT / "environment.cfg"
config.read(config_file)
CLIENT_ID = config["oauth"]["CLIENT_ID"]
CLIENT_SECRET = config["oauth"]["CLIENT_SECRET"]
TOKEN_URL = config["oauth"]["TOKEN_URL"]

# How many seconds before expiry to proactively refresh the token.
TOKEN_REFRESH_MARGIN = 30

def getUnixTime(secondsAgo=0):
    now = datetime.now(timezone.utc)
    now = now + timedelta(seconds=secondsAgo)
    print("Current time:", now)
    return int(now.timestamp())

class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = None

    def get_token(self):
        """Return a valid access token, refreshing automatically if needed."""
        if self.token and self.expires_at and datetime.now() < self.expires_at:
            return self.token
        return self._refresh()

    def _refresh(self):
        """Fetch a new access token from the OpenSky authentication server."""
        r = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        )
        r.raise_for_status()

        data = r.json()
        self.token = data["access_token"]
        expires_in = data.get("expires_in", 1800)
        self.expires_at = datetime.now() + timedelta(seconds=expires_in - TOKEN_REFRESH_MARGIN)
        return self.token

    def headers(self):
        """Return request headers with a valid Bearer token."""
        return {"Authorization": f"Bearer {self.get_token()}"}


# Create a single shared instance for your script.
tokens = TokenManager()

# Use it for any API call - the token is refreshed automatically.
begin = 1786827600
end = 1786831200
requestUrl = "https://opensky-network.org/api/flights/arrival?airport=EDDS&begin=" + str(begin) + "&end=" + str(end)
print("Request URL:", requestUrl)
response = requests.get(
    requestUrl,
    headers=tokens.headers(),
)
print(response.json())