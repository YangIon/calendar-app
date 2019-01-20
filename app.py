from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from calendar import Calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\Github\\calendar-app\\test.db'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)

events = []

@app.route("/")
def index():
    events = Event.query.all()
    current_month = date.today().month
    current_year = date.today().year
    cal = Calendar()
    calendar = []

    for week in cal.monthdatescalendar(current_year, current_month):
        new_week = []
        for day in week:
            new_day = [day]
            for event in events:
                if event.date == day:
                    new_day.append(event)
            new_week.append(new_day)
        calendar.append(new_week)

    return render_template("index.html", calendar=calendar)

@app.route("/add", methods=['GET', 'POST'])
def add():
    name_input = request.form['event'].strip()
    date_input = request.form['date'].strip()
    if name_input == "" or date_input == "":
        abort(401)

    date_components = date_input.split('-')
    year = int(date_components[0])
    month = int(date_components[1])
    day = int(date_components[2])

    date_object = date(year, month, day)

    event = Event(name=name_input, date=date_object)
    db.session.add(event)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<int:eventid>")
def delete(eventid):
    event = Event.query.get(eventid)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))

