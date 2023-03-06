# FRC Scouting app
This project is a simple, python-based (3.9+) webapp for scouting at FIRST Robotics Competition events. The server can either be hosted through a web hosting provider (e.g. Amazon Lightsail), or hosted locally at competitions with limited or nonexistent internet access.
  
## The basic idea
The conceptual model for this webapp is based on the idea of a **scouting admin** and a team of **scouters**. The scouting admin will generate **assignments** (team numbers) for each scouter, who will see that assignment pop up on their screen when it is assigned. The scouter will then collect data about their assigned team, and submit the form on-screen when done.
  
## Basic usage
At an FRC event, this server should be hosted either on the internet or on some form of LAN (bluetooth, ethernet, wifi hotspot, etc). The scouting admin uses a web browser to navigate to `[server]/admin/`, and each scouter navigates to `[server]/scouter/`. Each scouter will type in a nickname, and will be redirected to `[server]/scouter/[nickname]`, which registers them with the system, and they will each see a header labeled "Waiting for assignment". The scouting admin will see a realtime list of all active scouters on the system, with a text box beside each one. The scouting admin can enter a single team number into each of the text boxes (but not necessarily all), enter the match number, and click "Assign all".
  
At this point, the scouters will each see a form in which they can collect data about their assigned team (and see the team they are assigned), and can submit the data when done. This data is then collected and handled on the server device.
  
## Data collection and handling
The app has two methods of data collection: offline and online. See below.
### Offline mode
Offline mode can be specified by running the server with the `--offline` argument. This is for FRC competitions with limited or nonexistent internet connection. As results are uploaded, the data is stored in a ods-format spreadsheet document, which can be copied to other devices or uploaded to the cloud when an internet connection is present. The ods document location can be specified with the command line argument `--ods`, e.g. `--ods ./my_spreadsheet.ods`. **The ods file will not be overwritten when the server initializes**. It will just continue adding to the existing data in the ods file, so that the server can be restarted without any data loss.

DO NOT edit the ods document when the server is running, as it may lead to corrupted data or other problematic behavior. Instead, make a copy of the document to edit or insert charts.
### Online mode
Online requires that the server on which the webapp is hosted has a somewhat-reliable internet connection (hence the name). Online mode is selected when the server is run without the `--offline` command line argument, or when `--no-offline` is specified. Online mode requires the `--spreadsheet` argument, which is the id for an editable Google Sheets document:
```
https://docs.google.com/spreadsheets/d/1LqjrvDjERAL_7Efj0UyWA_y7UlqFgt_zP0CTL71YdSY/edit
                                       └──────────────── sheet id ────────────────┘
```
(here, the sheet id would be `1LqjrvDjERAL_7Efj0UyWA_y7UlqFgt_zP0CTL71YdSY`, and the server program would be invoked with `--spreadsheet 1LqjrvDjERAL_7Efj0UyWA_y7UlqFgt_zP0CTL71YdSY`).
  
Online mode requires use of the Google Sheets python API, which requires generating some credentials with the Google Cloud Platform. Generate a project there, enable the google sheets API, and download a JSON containing the OAuth key and client secret to `credentials.json`. When the server is first run in online mode (assuming you have proper credentials), it will put a url into stdout, and ask you to visit the URL and authenticate with the Google API. If you do so, it will save a persistent token file `token_creds.json` and start the web server. As data is collected, it will be saved into the Google Sheets document realtime for further analysis. **The Google Sheets document will not be overwritten.** The server will just add new data to the existing Google Sheets document, so the server can be restarted without any data loss.

Online mode also can **optionally** use the Custom Search Engine google API, for which you can generate an API key also on the google cloud platform. Use the Google Programmable Search Engine page to generate a CSE ID (or CX) with "Image search" enabled (or use the cx 334d7c38d111e4d21 if you want). Save the resulting key and CX to `cse_creds.json` in the following format: `{"key": "[key]", "cx": "[cx]"}`. **This step is optional**, but enables nice theme color generation for tabs in the Google Sheet document.

Even in online mode, the `--ods` option needs to be specified as a backup data target (in case of an API or network failure).