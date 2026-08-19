# FCC-Musberg

**FCC-Musberg** is an educational web application for a fictional **Flight Control Center in Musberg**, near Stuttgart, Germany. It was developed by school student **Daniel Khailov** to display the latest arrivals and departures for **Stuttgart Airport (STR/EDDS)**.

The project demonstrates practical skills in Python development, external API integration, JSON processing, web development, and multilingual location translation.

## Features

- Displays the latest arrivals at Stuttgart Airport
- Displays the latest departures from Stuttgart Airport
- Retrieves flight information through the AeroDataBox API
- Shows scheduled, revised, and actual flight times when available
- Shows flight status, airline, and flight number
- Shows origin and destination cities and countries
- Provides city and country names in English and Russian
- Uses `_cities.json` and alternative place names for translation
- Runs as a Python CGI application on a web server such as Apache

## Project Purpose

FCC-Musberg was created as a school and learning project. It demonstrates experience with:

- Python programming
- REST API authentication and integration
- Processing JSON responses
- Date and time processing
- Database-assisted translation
- English-Russian localization
- Connecting a Python backend to a web page
- Apache CGI deployment
- Git and GitHub repository management

## Technologies

- Python 3
- AeroDataBox API through RapidAPI
- Apache HTTP Server or XAMPP
- CGI
- HTML and CSS
- JSON
- Geographic and multilingual location data

## How It Works

1. `aerodatabox.py` reads the API key from `environment.cfg`.
2. The script requests current arrival and departure data from the AeroDataBox API.
3. It extracts relevant flight information, including flight number, airline, status, times, origin, and destination.
4. It uses `_cities.json` to enrich location data and provide English and Russian names.
5. The processed information is returned as an HTML page through CGI.

## Airport

- **Airport:** Stuttgart Airport
- **IATA code:** `STR`
- **ICAO code:** `EDDS`

## Prerequisites

- Python 3 installed on the server
- Apache with CGI enabled, for example through XAMPP
- An AeroDataBox API subscription and RapidAPI key
- All Python packages required by `aerodatabox.py`
- The files `aerodatabox.py`, `environment.cfg`, and `_cities.json`

## Installation and Deployment

### 1. Create `environment.cfg`

Create an `environment.cfg` file on the server. Add the `[aerodatabox]` section and store the API key in the `rapidapi_key` variable:

```ini
[aerodatabox]
rapidapi_key=YOUR_RAPIDAPI_KEY
```

Replace `YOUR_RAPIDAPI_KEY` with the actual API key provided through RapidAPI.

> **Security notice:** `environment.cfg` contains a secret. Do not commit it to a public GitHub repository, and make sure it cannot be downloaded through the web server. If an API key has already been published, revoke it and create a new one.

Add the file to `.gitignore`:

```gitignore
environment.cfg
```

### 2. Configure the path in `aerodatabox.py`

Make sure the path used by `aerodatabox.py` points to the actual location of `environment.cfg` on the server. Update the path in the script if necessary.

Example for XAMPP on Windows:

```python
config_file = r"C:\xampp\cgi-bin\environment.cfg"
```

Example for Apache on Linux:

```python
config_file = "/usr/lib/cgi-bin/environment.cfg"
```

Use an absolute server-side path where possible. Also verify that the path to `_cities.json` is correct.

### 3. Deploy the required files

Deploy these files to the server's configured `cgi-bin` directory:

```text
aerodatabox.py
environment.cfg
_cities.json
```

For example, a typical XAMPP installation on Windows may use:

```text
C:\xampp\cgi-bin\
```

Example deployment structure:

```text
cgi-bin/
├── aerodatabox.py
├── environment.cfg
└── _cities.json
```

The Python script must have permission to read both `environment.cfg` and `_cities.json`.

### 4. Prepare Python CGI execution

Ensure that Apache is configured to execute Python scripts in the `cgi-bin` directory.

The first line of `aerodatabox.py` should contain a valid path to the Python interpreter.

Example for Windows:

```python
#!C:/Python313/python.exe
```

Example for Linux:

```python
#!/usr/bin/env python3
```

On Linux, make the script executable:

```bash
chmod +x aerodatabox.py
```

The script must return a valid CGI content-type header before any HTML or other output:

```python
print("Content-Type: text/html; charset=utf-8")
print()
```

### 5. Run the application

Start Apache and open the CGI script in a browser:

```text
http://localhost/cgi-bin/aerodatabox.py
```

The script retrieves the latest arrivals and departures for Stuttgart Airport and returns the generated web page.

## Deployment Checklist

- Apache is running.
- CGI execution is enabled.
- Python is installed on the server.
- `aerodatabox.py` is in the configured `cgi-bin` folder.
- `environment.cfg` contains the `[aerodatabox]` section.
- `rapidapi_key` contains a valid AeroDataBox RapidAPI key.
- The `environment.cfg` path in `aerodatabox.py` is correct.
- The `_cities.json` path in `aerodatabox.py` is correct.
- The Python interpreter path in the shebang is valid.
- The required Python packages are installed.
- The script and data files have the required permissions.
- `environment.cfg` is excluded from Git and protected from public access.

## Troubleshooting

If Apache returns **500 Internal Server Error**:

1. Check the Apache error log.
2. Run `aerodatabox.py` directly from a terminal to identify Python errors.
3. Verify the Python interpreter path in the first line of the script.
4. Verify the paths to `environment.cfg` and `_cities.json`.
5. Confirm that `[aerodatabox]` and `rapidapi_key` are spelled correctly.
6. Confirm that the CGI content-type header is printed before any other output.
7. Confirm that all required packages are installed for the Python interpreter used by Apache.
8. On Linux, confirm that the script is executable and readable by the Apache user.

Example direct test:

```bash
python aerodatabox.py
```

## Repository Structure

```text
FCC-Musberg/
├── README.md
├── LICENSE
├── .gitignore
├── aerodatabox.py
├── _cities.json
└── environment.cfg      # Local secret; do not commit
```

## Limitations

- Flight data depends on AeroDataBox availability, coverage, and update frequency.
- Some flights may not include actual times or complete location details.
- API request limits depend on the selected AeroDataBox or RapidAPI subscription.
- This is an educational project and must not be used for operational air-traffic control, navigation, dispatch, or safety-critical decisions.
- FCC-Musberg is fictional and is not affiliated with Stuttgart Airport or an aviation authority.

## Future Improvements

- Automatic refresh of flight information
- Search and filtering by flight number, airline, status, or destination
- Visual indication of delayed, cancelled, landed, and departed flights
- Additional languages
- Airport weather information
- Route visualization on a map
- Caching to reduce API usage
- Automated tests
- Responsive design for mobile devices

## License

This project is free to use, study, modify, and distribute under the **MIT License**. See the `LICENSE` file for the complete license text.

## Author

**Daniel Khailov**  
School student and developer of FCC-Musberg

---

*FCC-Musberg is an independent educational project. AeroDataBox, RapidAPI, Stuttgart Airport, and other names or trademarks belong to their respective owners.*
