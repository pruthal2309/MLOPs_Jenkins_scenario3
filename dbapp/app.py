import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///records.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


with app.app_context():
    db.create_all()


def serialize_record(record):
    return {
        "id": record.id,
        "sepal_length": record.sepal_length,
        "sepal_width": record.sepal_width,
        "petal_length": record.petal_length,
        "petal_width": record.petal_width,
        "prediction": record.prediction,
        "created_at": record.created_at.isoformat(sep=" "),
    }


@app.route("/health", methods=["GET"])
def health():
    db.session.execute(text("SELECT 1"))
    return jsonify(status="healthy")


@app.route("/api/records", methods=["GET"])
def list_records():
    records = PredictionRecord.query.order_by(
        PredictionRecord.created_at.desc(), PredictionRecord.id.desc()
    ).all()
    return jsonify(records=[serialize_record(record) for record in records])


@app.route("/api/records", methods=["POST"])
def create_record():
    payload = request.get_json(silent=True) or {}
    try:
        record = PredictionRecord(
            sepal_length=float(payload["sepal_length"]),
            sepal_width=float(payload["sepal_width"]),
            petal_length=float(payload["petal_length"]),
            petal_width=float(payload["petal_width"]),
            prediction=str(payload["prediction"]),
        )
    except (KeyError, TypeError, ValueError):
        return jsonify(error="All measurements and prediction are required."), 400

    db.session.add(record)
    db.session.commit()
    db.session.refresh(record)
    return jsonify(record=serialize_record(record)), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)