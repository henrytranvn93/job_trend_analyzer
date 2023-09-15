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