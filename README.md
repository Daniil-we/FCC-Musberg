# FCC-Musberg

**FCC-Musberg** is an educational web application for a fictional **Flight Control Center in Musberg**, near Stuttgart, Germany. It was developed by school student **Daniel Khailov** to display the latest arrivals and departures for **Stuttgart Airport (STR)** and provide useful details about current flights.

The project demonstrates practical skills in Python development, integration with an external flight-data API, data processing, and multilingual location translation.

## Features

- Displays the latest **arrivals at Stuttgart Airport (STR)**
- Displays the latest **departures from Stuttgart Airport (STR)**
- Retrieves current flight information through the **AeroDataBox API**
- Shows scheduled and actual flight times, when available
- Shows the origin and destination airport or city
- Shows the origin and destination country
- Provides city and country names in both:
  - English
  - Russian
- Uses databases and alternative place names to translate standardized geographical information
- Presents the flight data on a lightweight local web page

## Project Purpose

FCC-Musberg was created as a school and learning project. Its purpose is to demonstrate experience with:

- Developing applications in **Python**
- Calling and processing data from **REST APIs**
- Working with JSON responses
- Handling current aviation data
- Translating city and country names with the help of databases
- Connecting a Python backend to a web page
- Structuring and maintaining source code in GitHub
- Protecting API credentials through configuration files and environment variables

## Technologies

The project may use the following technologies and services:

- **Python 3**
- **AeroDataBox API**, accessed through RapidAPI
- HTML and CSS
- JSON data processing
- Geographic or multilingual databases containing country, city, and alternative names
- A local web server, such as Apache with CGI support or a lightweight Python web server

## Geographic Data Source

The `_cities.json` file used by FCC-Musberg is derived from the external open-source GitHub project **[i18nGeoNamesDB](https://github.com/x88/i18nGeoNamesDB)**. The source project provides a multilingual geographic database containing countries, regions, and populated places, including English and Russian translations.

FCC-Musberg uses the prepared `_cities.json` file to match origin and destination locations returned by the AeroDataBox API and display city and country names in English and Russian. `_cities.json` is therefore not original geographic data created by the FCC-Musberg project.

The upstream `i18nGeoNamesDB` repository is archived and read-only. Its own license and attribution requirements continue to apply to data derived from it. See the upstream repository and its `LICENSE.md` file before redistributing or modifying the geographic dataset.

## How It Works

1. The Python application sends a request to the AeroDataBox API.
2. The API returns recent arrival and departure data for Stuttgart Airport.
3. The application extracts relevant information, such as:
   - Flight number
   - Airline
   - Scheduled time
   - Revised or actual time
   - Flight status
   - Origin
   - Destination
4. City and country codes or names are matched with database entries.
5. English and Russian location names are prepared for display.
6. The processed information is shown in a table on the web page.

## Airport

The application currently focuses on:

- **Airport:** Stuttgart Airport
- **IATA code:** `STR`
- **ICAO code:** `EDDS`

## Prerequisites

Before running the project, make sure the following components are available:

- Python 3 installed
- An active AeroDataBox API subscription or access key through RapidAPI
- The Python packages required by the project
- Access to the geographic data files or databases used for translation
- A local web server if the application is configured to run through CGI

## Installation and Deployment

The application is designed to run as a Python CGI script on a web server such as Apache.

### 1. Create `environment.cfg`

Create an `environment.cfg` file on the server. Add the `[aerodatabox]` section and store the AeroDataBox RapidAPI key in the `rapidapi_key` variable:

```ini
[aerodatabox]
rapidapi_key=YOUR_RAPIDAPI_KEY
```

Replace `YOUR_RAPIDAPI_KEY` with the actual API key provided through RapidAPI.

> **Security notice:** `environment.cfg` contains a secret. Do not commit it to a public GitHub repository, and make sure it cannot be downloaded through the web server. If an API key has already been published, revoke it and create a new one.

Add the configuration file to `.gitignore`:

```gitignore
environment.cfg
```

### 2. Configure the file paths in `aerodatabox.py`

Make sure the configuration path used by `aerodatabox.py` points to the actual location of `environment.cfg` on the server. Update it in the script if necessary.

Example for XAMPP on Windows:

```python
config_file = r"C:\xampp\cgi-bin\environment.cfg"
```

Also verify that the path used by the script for `_cities.json` is correct. The file contains geographic data derived from [i18nGeoNamesDB](https://github.com/x88/i18nGeoNamesDB).

### 3. Deploy the required files

Deploy the following files to the server's configured `cgi-bin` directory:

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
└── aerodatabox.py
FCC-Musberg/
├── environment.cfg
└── _cities.json
```

The Python script must have permission to read both `environment.cfg` and `_cities.json`.

### 4. Prepare Python CGI execution

Ensure that Apache is configured to execute Python scripts in the `cgi-bin` directory. The first line of `aerodatabox.py` must point to a valid Python interpreter.

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

The script retrieves the latest arrivals and departures for Stuttgart Airport, enriches the response with geographic information from `_cities.json`, and returns the generated web page.

### Deployment Checklist

- Apache is running and CGI execution is enabled.
- Python is installed on the server.
- `aerodatabox.py`, `environment.cfg`, and `_cities.json` are in the configured `cgi-bin` folder.
- `environment.cfg` contains the `[aerodatabox]` section.
- `rapidapi_key` contains a valid AeroDataBox RapidAPI key.
- The paths to `environment.cfg` and `_cities.json` in `aerodatabox.py` are correct.
- The Python interpreter path in the script is valid.
- Required Python packages and file permissions are in place.
- `environment.cfg` is excluded from Git and protected from public access.

### Troubleshooting

If Apache returns **500 Internal Server Error**:

1. Check the Apache error log.
2. Run `aerodatabox.py` directly from a terminal to identify Python errors.
3. Verify the Python interpreter path in the first line of the script.
4. Verify the paths to `environment.cfg` and `_cities.json`.
5. Confirm that `[aerodatabox]` and `rapidapi_key` are spelled correctly.
6. Confirm that the CGI content-type header is printed before any other output.
7. Confirm that all required Python packages are installed for the interpreter used by Apache.

## Example Information Displayed

A flight entry can include:

- Flight number and airline
- Arrival or departure status
- Scheduled time
- Actual or revised time
- Origin city and country
- Destination city and country
- English location names
- Russian location names

The availability and accuracy of individual fields depend on the data returned by the AeroDataBox API.

## Learning Outcomes

By developing FCC-Musberg, Daniel Khailov demonstrates skills in:

- Python programming
- API authentication and request handling
- External API integration
- Error handling and data validation
- Date and time processing
- Aviation data interpretation
- Database lookup and multilingual data mapping
- English-Russian localization
- Basic frontend and web-server integration
- Git and GitHub repository management

## Limitations

- Flight data depends on the availability, coverage, and update frequency of the AeroDataBox API.
- Some flights may not contain actual times, terminal information, or complete location details.
- API usage limits depend on the selected AeroDataBox or RapidAPI subscription.
- The application is an educational project and must not be used for operational air-traffic control, navigation, dispatch, or safety-critical decisions.
- FCC-Musberg is a fictional Flight Control Center and is not affiliated with Stuttgart Airport or an aviation authority.

## Future Improvements

Possible future enhancements include:

- Automatic refresh of flight information
- Search and filtering by flight number, airline, status, or destination
- Visual indication of delayed, cancelled, landed, and departed flights
- Additional languages
- Airport weather information
- Flight route visualization on a map
- Improved caching to reduce API usage
- Automated tests
- Responsive design for mobile devices
- Deployment to a hosted web environment

## License

The FCC-Musberg source code is free to use, study, modify, and distribute under the **MIT License**. See the `LICENSE` file for the complete license text.

### Third-party data

The `_cities.json` dataset is derived from the external [x88/i18nGeoNamesDB](https://github.com/x88/i18nGeoNamesDB) project and is not covered solely by the FCC-Musberg source-code license. Consult the upstream project's license and attribution information when using, modifying, or redistributing this data.

## Author

**Daniel Khailov**  
School student and developer of FCC-Musberg

---

*FCC-Musberg is an independent educational project. AeroDataBox, RapidAPI, Stuttgart Airport, and other names or trademarks belong to their respective owners.*
