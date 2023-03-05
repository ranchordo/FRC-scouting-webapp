import flask
import data_handler
import time

accepted_assignments = {}
waiting_assignments = {}

scouters = []

unprocessed_scouters_changes = False

def getActiveScouters():
    global scouters, unprocessed_scouters_changes
    new_scouters = []
    for scouter in scouters:
        if time.time() - scouter[1] < 600:
            new_scouters.append(scouter)
        else:
            unprocessed_scouters_changes = True
    scouters = new_scouters
    return scouters

counters_auto = [
    ("auto_low_pieces", "Pieces scored on low level"),
    ("auto_mid_pieces", "Pieces scored on mid level"),
    ("auto_high_pieces", "Pieces scored on high level")
]
counters_teleop = [
    ("teleop_low_pieces", "Pieces scored on low level"),
    ("teleop_mid_pieces", "Pieces scored on mid level"),
    ("teleop_high_pieces", "Pieces scored on high level")
]


def getAssignment(nickname):
    if nickname not in accepted_assignments:
        if nickname in waiting_assignments:
            accepted_assignments[nickname] = waiting_assignments[nickname]
            del waiting_assignments[nickname]
            return accepted_assignments[nickname]
        return "none"
    return accepted_assignments[nickname]

def addActiveScouter(nickname):
    global scouters, unprocessed_scouters_changes
    new_scouters = []
    no_removals = True
    for scouter in scouters:
        if scouter[0] != nickname:
            new_scouters.append(scouter)
        else:
            no_removals = False
    if no_removals:
        unprocessed_scouters_changes = True
    scouters = new_scouters
    scouters.append((nickname, time.time()))


def modify_app(app):
    @app.route("/scouter/", methods=['GET', 'POST'])
    def scouter_base():
        if flask.request.method == 'POST':
            return flask.redirect("/scouter/" + flask.request.form['nick'].lower() + "/")
        return flask.render_template("scouter_intro.html")

    @app.route("/scouter/<nickname>/", methods=['GET', 'POST'])
    def scouter_app(nickname):
        addActiveScouter(nickname)
        if flask.request.method == 'POST':
            data_handler.handleResponse(
                getAssignment(nickname), flask.request.form)
            if nickname in accepted_assignments:
                del accepted_assignments[nickname]
            return flask.redirect("/scouter/" + nickname + "/")
        return flask.render_template("scouter.html", nickname=nickname, counters_auto=counters_auto, counters_teleop=counters_teleop)

    @app.route("/scouter/<nickname>/assignment/")
    def get_assignment(nickname):
        return getAssignment(nickname)

    @app.route("/scouter/<nickname>/set_assignment/<assignment>/")
    def set_assignment(nickname, assignment):
        waiting_assignments[nickname] = assignment
        return "Success"
