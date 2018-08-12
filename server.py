"""Job Hunt app server"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from model import (User, Contact, ContactEvent, ContactCode, Company, Job,
                   JobEvent, JobCode, ToDo, ToDoCode, Salary, connect_to_db, db)
from datetime import datetime
from datetime import timedelta
import os
from random import choice

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


@app.route('/register', methods=['POST'])
def register_user():
    """Gets user input from registration form and checks against database.
    Then prompts user to login."""

    # get required user data from form
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']

    # create new user object
    new_user = User(fname=fname, lname=lname, email=email,
                    password=password, phone=phone)

    # before commiting to db, make sure user doesn't already exist
    verify_email = User.query.filter(User.email == new_user.email).all()

    if verify_email:
        return 'A user is already registered under that email address.'
    else:
        db.session.add(new_user)
        db.session.commit()
        return 'Thanks for registering! Please log in.'


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
        flash('No user exists with that email address.', 'error')
        return redirect('/')

    # if user exists but passwords don't match
    if user.password != password:
        flash('Incorrect password for the email address entered.', 'error')
        return redirect('/')

    # add user_id to session
    session['user_id'] = user.user_id

    # redirect to main dashboard page
    flash('May the job force be with you...', 'success')
    return redirect('/dashboard/jobs')


@app.route("/dashboard")
def dashboard():
    """logs the current user out"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        return redirect("/dashboard/jobs")


@app.route("/logout")
def logout():
    """logs the current user out"""

    # remove session from browser to log out
    del session['user_id']
    flash('Logged out.', 'success')
    return redirect("/")


# JOBS
#################################################################################
@app.route('/dashboard/jobs')
def show_active_jobs():
    """Shows list jobs the user is interested in, applied to, or interviewing for."""

    # get user_id from session and pass in companies
    user_id = session['user_id']
    user = User.query.filter(User.user_id == user_id).one()
    companies = user.companies

    # query for user job events, return list -- Look at created a db.relationship from users to jobs
    user_job_events = JobEvent.query.options(db.joinedload('jobs')).filter(JobEvent.user_id == user_id).order_by(desc('date_created')).all()
    job_event_ids = [event.job_event_id for event in user_job_events]

    # make a set of all job_ids and remove any that are inactive
    user_job_ids = set(job.job_id for job in user_job_events if job.jobs.active_status == True)

    # grab only the most recent events and todos for each job_id
    all_active_status = []
    all_todos = []
    for user_job_id in user_job_ids:
        # get all events for one job id
        events = [event for event in user_job_events if event.job_id == user_job_id]
        # find that latest event and add to list
        status = events[0]
        all_active_status.append(status)
        user_todo = ToDo.query.filter(ToDo.job_event_id == status.job_event_id, ToDo.active_status == True).first()
        if user_todo:
            all_todos.append(user_todo)

    return render_template('jobs-active.html', all_active_status=all_active_status, all_todos=all_todos, companies=companies)


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
        today = datetime.now()
        job_event = JobEvent(user_id=user_id,
                             job_id=job_id,
                             job_code=job_code,
                             date_created=today)
        db.session.add(job_event)

        todo_for_event = {'1': '1', '2': '2', '3': '3', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7'}
        todo_code = todo_for_event[job_code]
        find_code = ToDoCode.query.filter(ToDoCode.todo_code == todo_code).first()
        num_days = find_code.sugg_due_date
        due_date = today + timedelta(days=num_days)

        # activate todo for event
        new_todo = ToDo(job_event_id=job_event.job_event_id,
                        todo_code=todo_code,
                        date_created=today,
                        date_due=due_date,
                        active_status=True)
        db.session.add(new_todo)

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
        user = User.query.filter(User.user_id == user_id).one()
        companies = user.companies

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        user_job_events = JobEvent.query.options(db.joinedload('jobs')).filter(JobEvent.user_id == user_id).order_by(desc('date_created')).all()

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
                               all_archived=all_archived,
                               companies=companies)


@app.route('/dashboard/jobs/<job_id>')
def show_a_job(job_id):
    """Shows detailed info about a job"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        user_id = session['user_id']
        user = User.query.filter(User.user_id == user_id).one()
        companies = user.companies

        # get job from database and pre-load company data
        job = Job.query.filter(
            Job.job_id == job_id
            ).options(
            db.joinedload('companies')).first()

        # query for user job events, return list
        # Look at created a db.relationship from users to jobs
        job_status = JobEvent.query.options(db.joinedload('todos')).filter(JobEvent.user_id == user_id, JobEvent.job_id == job_id).order_by(desc('date_created')).order_by(desc('job_code')).all()

        # query for associated tasks, return list
        all_todos = []
        for status in job_status:
            todo = ToDo.query.filter(ToDo.job_event_id == status.job_event_id).options(db.joinedload('todo_codes')).first()
            all_todos.append(todo)

        if not job.avg_salary:
            metros = db.session.query(Salary.metro).group_by(Salary.metro).order_by(Salary.metro).all()
            job_titles = db.session.query(Salary.job_title).group_by(Salary.job_title).order_by(Salary.job_title).all()

        else:
            metros = ""
            job_titles = ""

        return render_template('job-info.html',
                               job=job,
                               metros=metros,
                               job_titles=job_titles,
                               job_status=job_status,
                               all_todos=all_todos,
                               companies=companies)


@app.route('/dashboard/jobs/edit', methods=['POST'])
def edit_a_job():
    """Allows user to edit info about a job"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get edited data from post request
        link = request.form['link']
        avg_salary = request.form['avg_salary']
        notes = request.form['notes']
        job_id = request.form['job_id']

        if not link:
            link = None
        elif link[:4] != 'http':
            link = ''.join(['http://', link])

        # get job from database, update, commit to db
        job = Job.query.filter(Job.job_id == job_id).first()
        job.link = link
        job.avg_salary = avg_salary
        job.notes = notes
        db.session.commit()

        results = {
            'link': job.link,
            'avg_salary': job.avg_salary,
            'notes': job.notes,
        }

        return jsonify(results)


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

        return job.avg_salary


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
        job_title = request.form['job_title']
        job_status = request.form['job_status']

        # look for optional data and add if it exists
        if request.form['job_link']:
            job_link = request.form['job_link']
            if not job_link:
                job_link = None
            elif job_link[:4] != 'http':
                job_link = ''.join(['http://', job_link])
        else:
            job_link = ""

        if request.form['job_notes']:
            job_notes = request.form['job_notes']
        else:
            job_notes = ""

        # look for company_id and find existing company
        # or get new company_name and create company object, add, commit
        if request.form['company_id']:
            company_id = int(request.form['company_id'])
            company = Company.query.filter(Company.company_id == company_id).first()
        elif request.form['company_name']:
            company_name = request.form['company_name']
            company = Company(name=company_name)
            db.session.add(company)
            db.session.commit()

        # create a new job object, add, commit
        job = Job(title=job_title, link=job_link, company_id=company.company_id,
                  active_status=True, notes=job_notes)
        db.session.add(job)
        db.session.commit()

        # create a job event to kick off job status, add, commit
        today = datetime.now()
        job_event = JobEvent(user_id=user_id, job_id=job.job_id,
                             job_code=job_status, date_created=today)
        db.session.add(job_event)
        db.session.commit()

        todo_for_event = {'1': '1', '2': '2', '3': '3', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7'}
        todo_code = todo_for_event[job_status]
        find_code = ToDoCode.query.filter(ToDoCode.todo_code == todo_code).first()
        num_days = find_code.sugg_due_date
        due_date = today + timedelta(days=num_days)

        # activate todo for event
        new_todo = ToDo(job_event_id=job_event.job_event_id,
                        todo_code=todo_code,
                        date_created=today,
                        date_due=due_date,
                        active_status=True)
        db.session.add(new_todo)
        db.session.commit()

        # return to active jobs and show confirmation
        flash('{} added to your jobs.'.format(job_title), 'success')
        return redirect('/dashboard/jobs')


# TO DO ITEMS
#################################################################################
@app.route('/dashboard/archive-task', methods=['POST'])
def archive_task():
    """Move a todo item from active to archived, so it no longer shows in the dashboard."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get todo_id from POST
        todo_id = request.form['todo_id']

        # find todo in database and change status
        todo = ToDo.query.filter(ToDo.todo_id == todo_id).first()
        todo.active_status = False
        db.session.commit()

    return 'Task archived!'


# COMPANIES
################################################################################
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
        user_job_events = JobEvent.query.options(db.joinedload('jobs')).filter(JobEvent.user_id == user_id).all()

        # make a set of all job ids
        user_job_ids = set(job.job_id for job in user_job_events)

        # make a list of all companies via job ids
        companies = {}
        for job_id in user_job_ids:
            job = Job.query.filter(Job.job_id == job_id).options(db.joinedload('companies')).first()
            count = Job.query.filter(Job.company_id == job.companies.company_id).count()
            companies[job.companies] = count

        # add companies from contacts
        user_contact_events = ContactEvent.query.options(db.joinedload('contacts')).filter(ContactEvent.user_id == user_id).all()
        user_contact_ids = set(contact.contact_id for contact in user_contact_events)
        for contact_id in user_contact_ids:
            contact = Contact.query.filter(Contact.contact_id == contact_id).options(db.joinedload('companies')).first()
            companies[contact.companies] = 0

        return render_template('companies.html', companies=companies)


@app.route('/dashboard/companies/<company_id>', methods=['GET'])
def show_a_company(company_id):
    """Show a company a user has interest in."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        edit = request.args.get('edit')

        # get user_id from session
        user_id = session['user_id']
        user = User.query.filter(User.user_id == user_id).one()
        companies = user.companies

        #get company info and pre-load jobs
        company = Company.query.filter(Company.company_id == company_id).options(db.joinedload('jobs')).options(db.joinedload('contacts')).first()
        # get list of active jobs and of arcived jobs
        active_jobs = [job for job in company.jobs if job.active_status]
        archived_jobs = [job for job in company.jobs if not job.active_status]

        states = ["", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                  "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                  "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                  "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        return render_template('company-info.html',
                               company=company,
                               edit=edit,
                               states=states,
                               companies=companies,
                               active_jobs=active_jobs,
                               archived_jobs=archived_jobs)


@app.route('/dashboard/companies/<company_id>', methods=['POST'])
def edit_a_company(company_id):
    """Edit a company a user has interest in."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        edit = request.args.get('edit')

        # get user_id from session
        user_id = session['user_id']
        user = User.query.filter(User.user_id == user_id).one()
        companies = user.companies

        # get company object to update
        company = Company.query.filter(Company.company_id == company_id).first()

        company.street = request.form['street']
        company.city = request.form['city']
        company.state = request.form['state']
        company.zipcode = request.form['zipcode']
        company.notes = request.form['notes']

        # if website doesn't have http or https in front, add it
        website = request.form['website']
        if not website:
            website = None
        elif website[:4] != 'http':
            website = ''.join(['http://', website])
        company.website = website

        db.session.commit()

        # get updated company info and pre-load jobs
        company = Company.query.filter(Company.company_id == company_id).options(db.joinedload('jobs')).first()

        # get list of active jobs and of arcived jobs
        active_jobs = [job for job in company.jobs if job.active_status]
        archived_jobs = [job for job in company.jobs if not job.active_status]

        states = ["", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                  "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                  "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                  "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        flash('Change made for {}'.format(company.name), 'success')
        return render_template('company-info.html',
                               company=company,
                               edit=edit,
                               states=states,
                               companies=companies,
                               active_jobs=active_jobs,
                               archived_jobs=archived_jobs)
        # can i pass companies by default - look at jinja context processors


# CONTACTS
#################################################################################
@app.route('/dashboard/contacts')
def show_all_contacts():
    """Show all contacts a user is connected to."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user
        user_id = session['user_id']
        user = User.query.filter(User.user_id == user_id).one()
        companies = user.companies

        # get all user events with all contacts
        contact_events = ContactEvent.query.filter(ContactEvent.user_id == user_id).all()

        # make a set of all contact_ids
        contact_ids = set(contact_event.contact_id for contact_event in contact_events)

        # grab all contact objects by contact_id
        contacts = []
        for contact_id in contact_ids:
            contact = Contact.query.filter(Contact.contact_id == contact_id).options(db.joinedload('companies')).first()
            contacts.append(contact)

        return render_template('contacts.html', contacts=contacts, companies=companies)


@app.route('/dashboard/contacts/<contact_id>', methods=['GET'])
def show_a_contact(contact_id):
    """Show one contact and all interactions."""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # get edit status
        edit = request.args.get('edit')

        # get contact (join companies) and all events
        contact = Contact.query.filter(Contact.contact_id == contact_id).options(db.joinedload('companies')).first()
        contact_events = ContactEvent.query.filter(ContactEvent.contact_id == contact_id).order_by(desc('date_created')).all()

        # find user existing companies based on job_events, jobs, companies
        # query for user job events, return list
        user_job_events = JobEvent.query.options(
            db.joinedload('jobs')
            ).filter(JobEvent.user_id == user_id).all()

        # make a set of all job ids
        user_job_ids = set(job.job_id for job in user_job_events)

        # make a list of all companies via job_ids
        companies = set()
        for job_id in user_job_ids:
            job = Job.query.filter(Job.job_id == job_id).options(db.joinedload('companies')).first()
            company = Company.query.filter(Company.company_id == job.company_id).first()
            companies.add(company)

        return render_template('contact-info.html',
                               edit=edit,
                               contact=contact,
                               contact_events=contact_events,
                               companies=companies)


@app.route('/dashboard/contacts/<contact_id>', methods=['POST'])
def edit_a_contact(contact_id):
    """Allows user to edit info about a contact"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # get edit status
        edit = request.args.get('edit')

        # get contact object to update
        contact = Contact.query.filter(Contact.contact_id == contact_id).options(db.joinedload('companies')).first()

        # get data from post request
        contact.fname = request.form['fname']
        contact.lname = request.form['lname']

        if request.form['email']:
            contact.email = request.form['email']
        if request.form['phone']:
            phone = "".join((request.form['phone']).split('-'))
            contact.phone = phone

        # look for company_id and find existing company
        # or get new company_name and create company object, add, commit
        if request.form['company_id']:
            company_id = int(request.form['company_id'])
            company = Company.query.filter(Company.company_id == company_id).first()
        elif request.form['company_name']:
            company_name = request.form['company_name']
            company = Company(name=company_name)
            db.session.add(company)
            db.session.commit()
        contact.company_id = company.company_id
        db.session.commit()

        # get updated contact info and events
        contact = Contact.query.filter(Contact.contact_id == contact_id).options(db.joinedload('companies')).first()
        contact_events = ContactEvent.query.filter(ContactEvent.contact_id == contact_id).order_by(desc('date_created')).all()

        # find user existing companies based on job_events, jobs, companies
        # query for user job events, return list
        user_job_events = JobEvent.query.options(
            db.joinedload('jobs')
            ).filter(JobEvent.user_id == user_id).all()

        # make a set of all job ids
        user_job_ids = set(job.job_id for job in user_job_events)

        # make a list of all companies via job_ids
        companies = set()
        for job_id in user_job_ids:
            job = Job.query.filter(Job.job_id == job_id).options(db.joinedload('companies')).first()
            company = Company.query.filter(Company.company_id == job.company_id).first()
            companies.add(company)

        flash('Change made for {} {}'.format(contact.fname, contact.lname), 'success')
        return render_template('contact-info.html',
                               edit=edit,
                               contact=contact,
                               contact_events=contact_events,
                               companies=companies)


@app.route('/dashboard/contacts/add', methods=['GET'])
def show_contact_add_form():
    """Allow user to add a contact"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get user_id from session
        user_id = session['user_id']

        # find user existing companies based on job_events, jobs, companies
        # query for user job events, return list
        user_job_events = JobEvent.query.options(
            db.joinedload('jobs')
            ).filter(JobEvent.user_id == user_id).all()

        # make a set of all job ids
        user_job_ids = set(job.job_id for job in user_job_events)

        # make a list of all companies via job_ids
        companies = set()
        for job_id in user_job_ids:
            job = Job.query.filter(Job.job_id == job_id).options(db.joinedload('companies')).first()
            company = Company.query.filter(Company.company_id == job.company_id).first()
            companies.add(company)

        return render_template('contacts-add.html', companies=companies)


@app.route('/dashboard/contacts/add', methods=['POST'])
def process_contact_form():
    """Allow user to add a contact"""

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get data from post request
        fname = request.form['fname']
        lname = request.form['lname']

        if request.form['email']:
            email = request.form['email']
        else:
            email = ""
        if request.form['phone']:
            phone = "".join((request.form['phone']).split('-'))
        else:
            phone = ""
        if request.form['notes']:
            notes = request.form['notes']
        else:
            notes = ""

        # look for company_id and find existing company
        # or get new company_name and create company object, add, commit
        if request.form['company_id']:
            company_id = int(request.form['company_id'])
            company = Company.query.filter(Company.company_id == company_id).first()
        elif request.form['company_name']:
            company_name = request.form['company_name']
            company = Company(name=company_name)
            db.session.add(company)
            db.session.commit()

        company_id = company.company_id

        # create new contact and commit to db
        new_contact = Contact(fname=fname, lname=lname, email=email, phone=phone,
                              company_id=company_id, notes=notes)
        db.session.add(new_contact)
        db.session.commit()

        # create initial contact event
        contact_code = request.form['contact_event']
        user_id = session['user_id']
        today = datetime.now()
        contact_event = ContactEvent(user_id=user_id, contacts=new_contact,
                                     contact_code=contact_code, date_created=today)
        db.session.add(contact_event)
        db.session.commit()

        flash('{} {} added to your contacts'.format(new_contact.fname, new_contact.lname), 'success')
        return redirect('/dashboard/contacts')


@app.route('/dashboard/contact-status', methods=['POST'])
def update_contact_status():
    """ Adds new contact events to database """

    # redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        # get contact_id, contact_code from POST and user_id from cookie
        contact_id = request.form['contact_id']
        contact_code = request.form['contact_code']
        user_id = session['user_id']

        # create job event
        today = datetime.now()
        contact_event = ContactEvent(user_id=user_id,
                                     contact_id=contact_id,
                                     contact_code=contact_code,
                                     date_created=today)
        db.session.add(contact_event)
        db.session.commit()

        return redirect('/dashboard/contacts')


# USER PROFILE
#################################################################################
@app.route('/dashboard/profile', methods=['GET'])
def show_user_profile():
    """Show user's profile and allow update to information."""

# redirect if user is not logged in
    if not session:
        return redirect('/')
    else:
        try:
            edit = request.args.get('edit')
        except KeyError:
            edit = 'edits-off'

        # find user in db
        user_id = session['user_id']
        user = User.query.filter(User.user_id == user_id).one()
        companies = user.companies

        # get user data to pass into charts
        user_job_events = JobEvent.query.options(db.joinedload('jobs')).filter(JobEvent.user_id == user_id).all()
        total_interested = len([event for event in user_job_events if event.job_code == 1])
        total_applied = len([event for event in user_job_events if event.job_code == 2])
        total_phone = len([event for event in user_job_events if event.job_code == 3])
        total_in_person = len([event for event in user_job_events if event.job_code == 4])
        total_job_offer = len([event for event in user_job_events if event.job_code == 5])

        user_analytics = {
            'interested': total_interested,
            'applied': total_applied,
            'phone': total_phone,
            'onsite': total_in_person,
            'offers': total_job_offer
        }

        return render_template('profile-tasks.html', user=user, edit=edit, companies=companies, user_analytics=user_analytics)



#################################################################################
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





























