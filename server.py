"""Job Hunt app server"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from model import (User, Contact, ContactEvent, ContactCode, Company, Job,
                   JobEvent, JobCode, ToDo, ToDoCode, Salary, connect_to_db, db)
from pprint import pprint
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

# If an undefined variable is used, Jinja2 will raise an error
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_landing_page():
    """Homepage."""

    return render_template('landing.html')


@app.route('/register', methods=['GET'])
def show_registration_form():
    """Shows registration form to user"""

    return render_template('register-form.html')


@app.route('/register', methods=['POST'])
def register_user():
    """Gets user input from registration form and checks against database.
    Then prompts user to login."""

    # get required user data from form
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    # try to get form data that isn't required
    try:
        phone = request.form['phone']
    except KeyError:
        phone = None

    # check to make sure this is working
    print(fname, lname, email, password, phone)

    # create new user object
    new_user = User(fname=fname, lname=lname, email=email, password=password, phone=phone)

    # before commiting to db, make sure user doesn't already exist
    verify_email = User.query.filter(User.email == new_user.email).all()

    if verify_email:
        flash('Sorry, a user is already registered under that email address.')
        return render_template('register-form.html')
    else:
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering! Please log in.')
        return redirect('/login')


@app.route('/login', methods=['GET'])
def show_login_form():
    """Shows login form to user"""

    return render_template('login-form.html')


@app.route('/login', methods=['POST'])
def login_user():
    """Gets user input from form and checks against database. If email and password
    match, start user session and take to main app page. Otherwise, prompt with flash
    message to try again."""

    # get required user data from form
    email = request.form['email']
    password = request.form['password']

    # search for user in db
    user = User.query.filter(User.email == email).first()

    # if user doesn't exist, redirect
    if not user:
        flash('No user exists with that email address.')
        return redirect('/login')

    # if user exists but passwords don't match
    if user.password != password:
        flash('Incorrect password for the email address entered.')
        return redirect('/login')

    # add user_id to session
    session['user_id'] = user.user_id

    # redirect to main dashboard page
    flash('May the job force be with you...')
    return redirect('/dashboard')


@app.route("/logout")
def logout():
    """logs the current user out"""

    # remove session from browser to log out
    del session['user_id']
    flash('Logged out.')
    return redirect("/")


@app.route('/dashboard')
def show_dashboard( ):
    """Shows default dashboard with jobs tracking"""

    return render_template('dashboard.html')


@app.route('/dashboard/jobs')
def show_active_jobs():
    """Shows list jobs the user is interested in, applied to, or interviewing for."""

    # get user_id from session
    user_id = session['user_id']

    # query for user job events, return list -- Look at created a db.relationship from users to jobs
    user_job_events = JobEvent.query.options(db.joinedload('jobs')).filter(JobEvent.user_id == user_id).order_by(desc('date_created')).all()

    # make a set of all job_ids and remove any that are inactive
    user_job_ids = set(job.job_id for job in user_job_events if job.jobs.active_status == True)

    # grab only the most recent events for each job_id
    all_active_status = []
    for user_job_id in user_job_ids:
        # get all events for one job id
        events = [event for event in user_job_events if event.job_id == user_job_id]
        # find that latest event and add to list
        status = events[0]
        all_active_status.append(status)

    # get active company objects
    companies = Company.query.filter(Company.company_id.in_(user_job_ids))

    return render_template('jobs-active.html',
                           all_active_status=all_active_status,
                           companies=companies)


@app.route('/dashboard/archive-job', methods=['POST'])
def archive_a_job():
    """Move job status from active to archive"""

    # get job_id from POST
    job_id = request.form['job_id']
    print(job_id)

    # find job in database
    job = Job.query.filter(Job.job_id == job_id).one()
    job.active_status = False

    return redirect('/dashboard/jobs')


if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')































