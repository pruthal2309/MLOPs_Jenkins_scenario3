import os
import pickle

import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DBAPP_URL = os.getenv("DBAPP_URL", "http://localhost:5001")

with open(os.path.join(os.path.dirname(__file__), "model.pkl"), "rb") as model_file:
    model = pickle.load(model_file)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return redirect(url_for("index"))

    try:
        values = {
            "sepal_length": float(request.form["sepal_length"]),
            "sepal_width": float(request.form["sepal_width"]),
            "petal_length": float(request.form["petal_length"]),
            "petal_width": float(request.form["petal_width"]),
        }
    except (KeyError, ValueError):
        return render_template(
            "result.html",
            prediction="Invalid input. Please enter valid numbers for all fields.",
            inputs=None,
        )

    prediction = str(model.predict([list(values.values())])[0])
    save_error = None
    try:
        response = requests.post(
            f"{DBAPP_URL}/api/records",
            json={**values, "prediction": prediction},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException:
        save_error = "Prediction completed, but it could not be saved. Try again later."

    inputs = {
        "Sepal Length": values["sepal_length"],
        "Sepal Width": values["sepal_width"],
        "Petal Length": values["petal_length"],
        "Petal Width": values["petal_width"],
    }
    return render_template(
        "result.html", prediction=prediction, inputs=inputs, save_error=save_error
    )


@app.route("/records", methods=["GET"])
def records():
    try:
        response = requests.get(f"{DBAPP_URL}/api/records", timeout=5)
        response.raise_for_status()
        records = response.json()["records"]
        error = None
    except (requests.RequestException, ValueError, KeyError):
        records = []
        error = "Could not load prediction records. Please try again later."
    return render_template("records.html", records=records, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)