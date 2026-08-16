import sys
from datetime import datetime
from zoneinfo import ZoneInfo

print("Content-Type: text/html; charset=utf-8")
print()

now = datetime.now(ZoneInfo("Europe/Berlin"))

print("<!DOCTYPE html>")
print("<html>")
print("<head><title>Python CGI Test</title></head>")
print("<body>")
print("<h1>Python is running through XAMPP Apache</h1>")
print(f"<p>Python version: {sys.version}</p>")
print(f"<p>Berlin time: {now:%Y-%m-%d %H:%M:%S %Z}</p>")
print("</body>")
print("</html>")