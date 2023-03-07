import flask

def modify_app(app):
    @app.route("/water.css")
    def water():
        return flask.send_from_directory("static","water.css")