from flask import Flask, render_template, request
import requests
import sys
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Adjusting the DATABASE_URL for SQLAlchemy compatibility
DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)

# Database Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        jobs = fetch_jobs(keyword)
        return render_template('report.html', jobs=jobs)
    return render_template('index.html')

def fetch_jobs(keyword):
    # Placeholder for an API call
    job_data = [{'title': 'Software Engineer', 'company': 'Tech Corp', 'location': 'NYC'}]
    for job in job_data:
        new_job = Job(title=job['title'], company=job['company'], location=job['location'])
        db.session.add(new_job)
    db.session.commit()
    return job_data

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
    print('Initialized the database.')

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    if "initdb" in sys.argv:
        init_db()
    else:
        app.run(debug=True)
