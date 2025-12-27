import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# -------------------------------------------------

# ---------------- TABLE MODEL --------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_id = db.Column(db.String(50))
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    income = db.Column(db.Float)
    city = db.Column(db.String(100))
    acquisition = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    department = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# -------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json

        student = Student(
            serial_id=data.get("studentId"),
            full_name=data.get("fullName"),
            phone=data.get("phone"),
            email=data.get("email"),
            income=float(data.get("income")),
            city=data.get("city"),
            acquisition=data.get("acquisition"),
            gender=data.get("gender"),
            department=data.get("department")
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({"status": "success"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400

# -------- CREATE TABLES ON STARTUP --------
with app.app_context():
    db.create_all()
# -----------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)