from flask import Flask, render_template, jsonify, request
from time import sleep
from random import randint

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def load_data():

    sleep(2)
    data = [{"text": randint(0, 10)} for v in range(1, 6)]

    if request.is_json:
        return jsonify(data)

    return render_template("data.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        sleep(2)

        name = request.json.get("name") if request.is_json else request.form.get("name")
        email = (
            request.json.get("email") if request.is_json else request.form.get("email")
        )

        if request.is_json:

            print(request.json)

            # name = request.json.get("name")
            # email = request.json.get("email")

            return jsonify({"name": name, "email": email})

        # name = request.form.get("name")
        # email = request.form.get("email")

        return render_template("result.html", name=name, email=email)

    return render_template("index.html")


app.run(debug=True)
