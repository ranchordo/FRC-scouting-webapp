import flask
import scouter

last_match = 0

def modify_app(app):
    @app.route("/admin/",methods=['GET','POST'])
    def admin_base():
        global last_match
        scouter.unprocessed_scouters_changes = False
        if flask.request.method == 'POST':
            last_match += 1
            match_number = last_match
            try:
                match_number = int(flask.request.form['match_number'])
                last_match = match_number
            except ValueError:
                pass
            for key in flask.request.form:
                if key != "match_number":
                    scouter.waiting_assignments[key] = flask.request.form[key] + ", match #" + str(match_number)
        scouters = [i[0] for i in scouter.getActiveScouters()]
        return flask.render_template("admin.html", scouters = scouters, num_scouters = len(scouters))
    @app.route("/admin/scouters_update/")
    def admin_update():
        return ("reload" if scouter.unprocessed_scouters_changes else "up to date")