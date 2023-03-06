from flask import Flask
import scouter
import files
import admin
import argparse
import data_handler
import os
import gsheets


def create_app():
    parser = argparse.ArgumentParser(
        prog="FRC Scouting Webapp", description="Simple flask webapp designed for online and offline FRC event scouting.")
    parser.add_argument('--offline', action=argparse.BooleanOptionalAction)
    parser.add_argument('--spreadsheet')

    args = parser.parse_args()

    if args.offline:
        if args.spreadsheet is not None:
            print("Spreadsheet specified in offline mode. Cannot proceed.")
            os._exit(1)
    else:
        if args.spreadsheet is None:
            print("No spreadsheet specified in online mode. Cannot proceed.")
            os._exit(1)

    data_handler.spreadsheetId = args.spreadsheet
    data_handler.online = (False if args.offline else True)
    data_handler.init()

    app = Flask(__name__)

    @app.route("/")
    def baseroute():
        return "No"
    scouter.modify_app(app)
    files.modify_app(app)
    admin.modify_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=80)
