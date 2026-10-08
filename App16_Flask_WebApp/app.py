import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, render_template, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()

app = Flask(__name__, instance_path=str(BASE_DIR / "instance"))
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(50), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        date = request.form.get("date")
        date_obj = datetime.strptime(date, "%Y-%m-%d").astimezone()
        occupation = request.form.get("occupation")

        form = Form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=date_obj,
            occupation=occupation,
        )
        db.session.add(form)
        db.session.commit()

        message_body = f"""
Thank you for your submission, {first_name}
Here is your data: 
First Name: {first_name}
Last Name: {last_name}
Date of Submission: {date}
Thank you
"""

        message = Message(
            subject="New form submission",
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]],
            body=message_body,
        )

        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
