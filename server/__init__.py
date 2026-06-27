from flask import Flask, make_response, render_template
import os
import subprocess

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    return app


app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/candidate/refresh")
def refreshCandidate():
    process = subprocess.Popen(["venv/bin/python", "board-bot.py", "--capture-candidate"], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True)

    response = make_response(process.stdout)
    response.mimetype = "text/plain"

    return response


@app.post("/refresh")
def refresh():
    return render_template("refresh.html")


@app.get("/refresh/execute")
def refreshCommand():
    process = subprocess.Popen(["venv/bin/python", "board-bot.py"], stdout=subprocess.PIPE, text=True)

    response = make_response(process.stdout)
    response.mimetype = "text/plain"

    return response
