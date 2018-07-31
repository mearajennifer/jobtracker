"""Job Hunt app server"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from model import (User, Contact, ContactEvent, ContactCode, Company, Job,
                   JobEvent, JobCode, ToDo, ToDoCode, Salary, connect_to_db, db)
from datetime import datetime
from datetime import date
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

# If an undefined variable is used, Jinja2 will raise an error
app.jinja_env.undefined = StrictUndefined


# LANDING PAGE, REGISTER, LOGIN, LOGOUT
#################################################################################
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
    new_user = User(fname=fname, lname=lname, email=email,
                    password=password, phone=phone)

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
    """Gets user input from form and checks against database. If email and
    password match, start user session and take to main app page. Otherwise,
    prompt with flash message to try again."""

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
    return redirect('/dashboard/jobs')


@app.route("/logout")
def logout():
    """logs the current user out"""

    # remove session from browser to log out
    del session['user_id']
    flash('Logged out.')
    return redirect("/")


# JOBS
#################################################################################
@app.route('/dashboard/jobs')
def show_active_jobs():
    """Shows list jobs the user is connected to."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        user_job_events = JobEvent.query.options(db.joinedload('jobs')).filter(JobEvent.user_id == user_id).order_by(desc('date_created')).all()

        # make a set of all job_ids and remove any that are inactive
        user_job_ids = set(job.job_id for job in user_job_events
                           if job.jobs.active_status == True)

        # grab only the most recent events for each job_id
        all_active_status = {}
        for user_job_id in user_job_ids:
            # get all events for one job id
            events = [event for event in user_job_events if event.job_id == user_job_id]
            # find that latest event and add to list
            status = events[0]
            company = Company.query.filter(
                Company.company_id == status.jobs.company_id).first()
            all_active_status[status] = company

        return render_template('jobs-active.html',
                               all_active_status=all_active_status)


@app.route('/dashboard/job-status', methods=['POST'])
def update_job_status():
    """Move job status from active to archive"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get job_id, job_code from POST and user_id from cookie
        job_id = request.form['job_id']
        job_code = request.form['job_code']
        user_id = session['user_id']

        # create job event
        today = datetime.date(datetime.now())
        job_event = JobEvent(user_id=user_id,
                             job_id=job_id,
                             job_code=job_code,
                             date_created=today)
        db.session.add(job_event)

        # find job in database and archive if necessary
        job = Job.query.filter(Job.job_id == job_id).first()
        if int(job_code) > 5:
            job.active_status = False

        db.session.commit()

        return redirect('/dashboard/jobs')


@app.route('/dashboard/jobs/archived')
def show_archived_jobs():
    """ Shows a list of archived jobs the user is no longer tracking."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        user_job_events = JobEvent.query.options(
            db.joinedload('jobs')
            ).filter(JobEvent.user_id == user_id
                     ).order_by(desc('date_created')).all()

        # make a set of all job_ids and remove any that are inactive
        user_job_ids = set(job.job_id for job in user_job_events
                           if job.jobs.active_status == False)

        # grab only the most recent events for each job_id
        all_archived = {}
        for user_job_id in user_job_ids:

            # get all events for one job id
            events = [event for event in user_job_events
                      if event.job_id == user_job_id]

            # find that latest event and add to list
            status = events[0]
            company = Company.query.filter(
                Company.company_id == status.jobs.company_id).first()
            all_archived[status] = company

        return render_template('jobs-archive.html',
                               all_archived=all_archived)


@app.route('/dashboard/jobs/<job_id>', methods=['GET'])
def show_a_job(job_id):
    """Shows detailed info about a job"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        edit = request.args.get('edit')
        user_id = session['user_id']

        # get job from database and pre-load company data
        job = Job.query.filter(
            Job.job_id == job_id
            ).options(
            db.joinedload('companies')).first()

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        job_status = JobEvent.query.filter(JobEvent.user_id == user_id,
                                           JobEvent.job_id == job_id
                                           ).order_by(desc('date_created')).order_by(desc('job_code')).all()

        if not job.avg_salary:
            metros = db.session.query(Salary.metro).group_by(Salary.metro).order_by(Salary.metro).all()
            job_titles = db.session.query(Salary.job_title).group_by(Salary.job_title).order_by(Salary.job_title).all()

        else:
            metros = None
            job_titles = None

        return render_template('job-info.html',
                               job=job,
                               metros=metros,
                               job_titles=job_titles,
                               job_status=job_status,
                               edit=edit)


@app.route('/dashboard/jobs/<job_id>', methods=['POST'])
def edit_a_job(job_id):
    """Allows user to edit info about a job"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        edit = request.form.get('edit')
        link = request.form.get('link')
        avg_salary = request.form.get('avg_salary')
        notes = request.form.get('notes')

        # get job from database and pre-load company data
        job = Job.query.filter(
            Job.job_id == job_id
            ).options(
            db.joinedload('companies')).first()

        job.link = link
        job.avg_salary = avg_salary
        job.notes = notes

        db.session.commit()

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        job_status = JobEvent.query.filter(JobEvent.user_id == user_id,
                                           JobEvent.job_id == job_id
                                           ).order_by(desc('date_created')).order_by(desc('job_code')).all()

        if not job.avg_salary:
            metros = db.session.query(Salary.metro).group_by(Salary.metro).order_by(Salary.metro).all()
            job_titles = db.session.query(Salary.job_title).group_by(Salary.job_title).order_by(Salary.job_title).all()
        else:
            metros = None
            job_titles = None

        return render_template('job-info.html',
                               job=job,
                               metros=metros,
                               job_titles=job_titles,
                               job_status=job_status,
                               edit=edit)


@app.route('/dashboard/jobs/salary', methods=['POST'])
def get_salary():
    """Finds salary for job title in metro area"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get metro and job_title selections
        metro = request.form['metro']
        job_title = request.form['job_title']
        job_id = request.form['job_id']

        salary = Salary.query.filter(
            Salary.metro == metro,
            Salary.job_title == job_title).one()

        job = Job.query.filter(Job.job_id == job_id).first()
        job.avg_salary = salary.avg_salary

        db.session.commit()

        return redirect('/dashboard/jobs/' + job_id)


@app.route('/dashboard/jobs/add', methods=['GET'])
def show_job_add_form():
    """Allow user to add a job"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        user_job_events = JobEvent.query.options(
            db.joinedload('jobs')
            ).filter(JobEvent.user_id == user_id).all()

        # make a set of all job ids
        user_job_ids = set(job.job_id for job in user_job_events)

        # make a list of all companies via job_ids
        companies = []
        for job_id in user_job_ids:
            job = Job.query.filter(
                Job.job_id == job_id
                ).options(
                db.joinedload('companies')
                ).first()
            companies.append(job.companies)

        return render_template('jobs-add.html', companies=companies)

@app.route('/dashboard/jobs/add', methods=['POST'])
def process_job_form():
    """Allow user to add a job"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # get data from form
        company_name = request.form['company_name']
        job_title = request.form['job_title']
        job_status = request.form['job_status']

        try:
            job_link = request.form['job_link']
            job_notes = request.form['job_notes']
        except KeyError:
            job_link = ""
            job_notes = ""

        # create company
        company = Company(name=company_name)
        db.session.add(company)
        db.session.commit()

        job = Job(title=job_title, link=job_link, company_id=company.company_id,
                  active_status=True, notes=job_notes)
        db.session.add(job)
        db.session.commit()

        today = datetime.date(datetime.now())
        job_event = JobEvent(user_id=user_id, job_id=job.job_id,
                             job_code=job_status, date_created=today)
        db.session.add(job_event)
        db.session.commit()

        return redirect('/dashboard/jobs')


# COMPANIES
#################################################################################
@app.route('/dashboard/companies')
def show_all_companies():
    """Show all companies a user has interest in."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        user_job_events = JobEvent.query.options(
            db.joinedload('jobs')
            ).filter(JobEvent.user_id == user_id).all()

        # make a set of all job ids
        user_job_ids = set(job.job_id for job in user_job_events)

        # make a list of all companies via job ids
        companies = {}
        for job_id in user_job_ids:
            job = Job.query.filter(
                Job.job_id == job_id
                ).options(
                db.joinedload('companies')
                ).first()
            count = Job.query.filter(
                Job.company_id == job.companies.company_id).count()
            companies[job.companies] = count

        return render_template('companies.html', companies=companies)


@app.route('/dashboard/companies/<company_id>', methods=['GET'])
def show_a_company(company_id):
    """Show a company a user has interest in."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        edit = request.args.get('edit')

        #get company info and pre-load jobs
        company = Company.query.filter(
            Company.company_id == company_id
            ).options(db.joinedload('jobs')).first()

        return render_template('company-info.html', company=company, edit=edit)


@app.route('/dashboard/companies/<company_id>', methods=['POST'])
def edit_a_company(company_id):
    """Show a company a user has interest in."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        edit = request.args.get('edit')

        # get company object to update
        company = Company.query.filter(
            Company.company_id == company_id
            ).options(db.joinedload('jobs')).first()

        company.street = request.form['street']
        company.city = request.form['city']
        company.state = request.form['state']
        company.zipcode = request.form['zipcode']
        company.website = request.form['website']
        company.notes = request.form['notes']

        db.session.commit()

        # get updated company info and pre-load jobs
        company = Company.query.filter(
            Company.company_id == company_id
            ).options(db.joinedload('jobs')).first()

        flash(u"Change made for {}".format(company.name), 'success')
        return render_template('company-info.html', company=company, edit=edit)


@app.route('/dashboard/companies/add')
def add_a_company():
    """Allow user to add a company"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        pass


# CONTACTS
#################################################################################
@app.route('/dashboard/contact')
def show_all_contacts():
    """Show all contacts a user is connected to."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        pass


@app.route('/dashboard/contact/<contact_id>')
def show_a_contact(contact_id):
    """Show one contacts a user is connected to and all interactions."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        pass


@app.route('/dashboard/contact/add')
def add_a_contact():
    """Allow user to add a contact"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        pass


# USER PROFILE
#################################################################################
@app.route('/dashboard/user')
def show_user_profile():
    """Show user's profile and allow update to information."""

# redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        pass


if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=5000, host='0.0.0.0')





























