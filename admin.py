import flask
import scouter

def modify_app(app):
    @app.route("/admin/",methods=['GET','POST'])
    def admin_base():
        scouter.unprocessed_scouters_changes = False
        if flask.request.method == 'POST':
            for key in flask.request.form:
                scouter.waiting_assignments[key] = flask.request.form[key]
        scouters = [i[0] for i in scouter.getActiveScouters()]
        return flask.render_template("admin.html", scouters = scouters, num_scouters = len(scouters))
    @app.route("/admin/scouters_update/")
    def admin_update():
        return ("reload" if scouter.unprocessed_scouters_changes else "up to date")