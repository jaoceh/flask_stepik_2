import json
from random import randint

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.secret_key = 'matvey'

with open ('data/times.json') as file:
    times = json.load(file)

with open('data/teachers.json') as file:
    teachers = json.load(file)

with open('data/weekdays.json') as file:
    weekdays = json.load(file)

with open('data/goals.json') as file:
    goals = json.load(file)

for teacher in teachers:
    formatted_goals = []
    for goal in teacher['goals']:
        for k,v in goals.items():
            if goal == k:
                formatted_goals.append(v)
    teacher['goals'] = formatted_goals


class BookingForm(FlaskForm):
    name = StringField("Вас зовут", [InputRequired()])
    phone = StringField("Ваш телефон", [InputRequired(), Length(min=10, max=20)])


class RequestForm(FlaskForm):
    goals = RadioField('goals', validators=[InputRequired()],choices=[(k,v)for k,v in goals.items()])
    time = RadioField('time', choices=[(k,v) for k,v in times.items()])
    name = StringField("Вас зовут", [InputRequired()])
    phone = StringField("Ваш телефон", [InputRequired(), Length(min=10, max=20)])


@app.route('/')
def main():
    pinned_teachers = []
    r_ids = []
    while len(r_ids) < 6:
        id = randint(1,11)
        r_ids.append(id)
        r_ids = list(set(r_ids))
    for id in r_ids:
        for teacher in teachers:
            if teacher['id'] == id:
                pinned_teachers.append(teacher)
    return render_template('index.html',
                           goals=goals,
                           teachers=pinned_teachers)

@app.route('/all_teachers')
def all_teachers():
    return render_template('all_teachers.html',
                           goals=goals,
                           teachers=teachers)

@app.route('/goals/<goal>')
def goal(goal):
    for k,v in goals.items():
        if k == goal:
            formatted_goal = v
    needed_teachers = []
    for teacher in teachers:
        if formatted_goal in teacher['goals']:
            needed_teachers.append(teacher)
    return render_template('goal.html',
                           formatted_goal=formatted_goal,
                           needed_teachers=needed_teachers)

@app.route('/profiles/<id>')
def profile(id):
    for teacher in teachers:
        if teacher['id'] == int(id):
            profile = teacher

    return render_template('profile.html',
                           profile=profile,
                           weekdays=weekdays)

@app.route('/request')
def make_request():
    form = RequestForm()
    return render_template('request.html',
                           form=form,
                           times=times)

@app.route('/request_done', methods=['POST','GET'])
def request_done():
    form = RequestForm()
    if request.method == 'POST':
        goal = form.goals.data
        time = form.time.data
        name = form.name.data
        phone = form.phone.data
        request_ = {}
        request_['clientGoal'] = goal
        request_['clientTime'] = time
        request_['clientName'] = name
        request_['clientPhone'] = phone
        with open('data/requests.json') as file:
            requests = json.load(file)
        requests.append(request_)
        with open('data/requests.json','w') as file:
            json.dump(requests, file, indent=4)
        return render_template('request_done.html',
                        name=name,
                        phone=phone,
                        time=time,
                        goal=goal)
    return render_template('request.html',
                           form=form)

@app.route('/booking/<id>/<day>/<time>', methods=['POST','GET'])
def booking(id,day,time):
    id=int(id)
    for teacher in teachers:
        if teacher['id'] == int(id):
            name = teacher['name']
            picture = teacher['picture']
    form = BookingForm()
    return render_template('booking.html',
                           name=name,
                           day=day,
                           time=time,
                           picture=picture,
                           form=form,
                           id=id,
                           weekdays=weekdays)

@app.route('/booking_done', methods=['POST', 'GET'])
def booking_done():
    form = BookingForm()

    if request.method == 'POST':
        name = form.name.data
        phone = form.phone.data
        time = request.form['clientTime']
        id = request.form['clientTeacher']
        day = request.form['clientWeekday']
        booking = {}
        booking['clientTeacher'] = id
        booking['clientTime'] = time
        booking['clientWeekday'] = day
        booking['clientName'] = name
        booking['clientPhone'] = phone
        with open('data/bookings.json') as file:
            bookings = json.load(file)
        bookings.append(booking)
        with open('data/bookings.json','w') as file:
            json.dump(bookings, file, indent=4)
        return render_template('booking_done.html',
                               name=name,
                               phone=phone,
                               time=time,
                               id=id,
                               day=day,
                               weekdays=weekdays)
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)