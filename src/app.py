#!/usr/bin/env python3
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'

db = SQLAlchemy(app)

@app.route("/")
def main():
    current_temperature = get_temperature()
    if current_temperature is not None:
        try:
            new_entry = Weather(temperature=current_temperature)
            db.session.add(new_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error:", e)
    return '''
     <form action="/echo_user_input" method="POST">
        <p>Input your name and submit to see the greeting!</p>
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    current_temperature = get_temperature()
    return f"Hello {input_text}! Nice to meet you. Temperature at Vancouver now: {current_temperature} Celcius."

class Weather(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    temperature = db.Column(db.Float, nullable=False)


def get_temperature():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=49.2497&longitude=-123.1193&hourly=temperature_2m&current_weather=true")
    return response.json()["current_weather"]["temperature"]
    
def init_db():
    with app.app_context():
        db.create_all()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.cli.command('initdb')
def init_db_command():
    """Initializes the database tables."""
    init_db()
    print('Initialized the database.')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)