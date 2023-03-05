from flask import Flask
import scouter, files, admin

def create_app():
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
    app.run(debug = False, host = '0.0.0.0', port = "80")