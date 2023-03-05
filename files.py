import flask

def modify_app(app):
    @app.route("/water.css")
    def water():
        return flask.send_from_directory("static","water.css")
    @app.route("/assignment-worker.js")
    def assignment_worker():
        with open("./static/assignment-worker.js",'r') as f:
            output = f.read()
            return flask.Response(output, mimetype = "text/javascript")