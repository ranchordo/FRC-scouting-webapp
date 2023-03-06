import requests
import os
import gsheets
import imgsearch
import threading
from pyexcel_ods3 import save_data, get_data
from collections import OrderedDict

counters_auto = [
    ("auto_low_pieces", "Pieces scored on low level", lambda x: x * 3),
    ("auto_mid_pieces", "Pieces scored on mid level", lambda x: x * 4),
    ("auto_high_pieces", "Pieces scored on high level", lambda x: x * 6),
    ("auto_charging_station", "Charging station (0 - not docked or engaged, 1 - docked, 2 - engaged)",
     lambda x: (12 if x >= 2 else 8 * x))
]
counters_teleop = [
    ("teleop_low_cones", "Cones scored on low level", lambda x: x * 2),
    ("teleop_low_cubes", "Cubes scored on low level", lambda x: x * 2),
    ("teleop_mid_cones", "Cones scored on mid level", lambda x: x * 3),
    ("teleop_mid_cubes", "Cubes scored on mid level", lambda x: x * 3),
    ("teleop_high_cones", "Cones scored on high level", lambda x: x * 5),
    ("teleop_high_cubes", "Cubes scored on high level", lambda x: x * 5),
    ("teleop_links_made", "Links made", lambda x: x * 5),
    ("teleop_charging_station", "Charging station (0 - not docked or engaged, 1 - docked, 2 - engaged)",
     lambda x: (10 if x >= 2 else 6 * x))
]

spreadsheetId = None
odsFile = None
online = False


def init():
    if online:
        try:
            requests.get("http://1.1.1.1", timeout=1)
        except:
            print(
                "Online mode specified, but system is not connected to the internet. Cannot proceed.")
            os._exit(1)
        gsheets.initialize()
    else:
        if not os.path.exists(odsFile):
            save_data(odsFile, OrderedDict())


def computeTotal(response, counters):
    total = 0
    for key in response:
        for counter in counters:
            if counter[0] in key:
                try:
                    total += counter[2](int(response[key]))
                    break
                except ValueError:
                    pass
    return total


def createTeamSheet(team):
    row = ["Match #"]
    for counter in counters_auto:
        row.append(counter[0])
    for counter in counters_teleop:
        row.append(counter[0])
    row.append("Notes?")
    row.append("Auto total")
    row.append("Teleop total")
    row.append("Total")
    if online and str(team) not in gsheets.getSheetNames():
        color = imgsearch.getTeamColor(team)
        gsheets.addSheet(str(team), tuple(color))
        gsheets.appendRow(team, row)
    if not online and str(team) not in get_data(odsFile).keys():
        data = get_data(odsFile)
        data.update({str(team): [row]})
        save_data(odsFile, data)


def addRow(team, row):
    if online:
        gsheets.appendRow(team, row)
    else:
        data = get_data(odsFile)
        newdata = data[str(team)] + [row]
        data.update({str(team): newdata})
        save_data(odsFile, data)


def handleNewRow(team, row):
    createTeamSheet(team)
    addRow(team, row)


def handleResponse(assignment, response):
    row = ['?']
    try:
        row = [assignment.split(", match #")[1]]
    except IndexError:
        pass
    for val in response.values():
        row.append(val)
    auto_total = computeTotal(response, counters_auto)
    row.append(str(auto_total))
    teleop_total = computeTotal(response, counters_teleop)
    row.append(str(teleop_total))
    row.append(str(teleop_total + auto_total))
    threading.Thread(target=lambda: handleNewRow(
        assignment.split(", match #")[0], row)).start()
