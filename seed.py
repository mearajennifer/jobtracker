"""Utility file to seed job hunt app database from created, sample, and Glassdoor data in /data folder"""


from sqlalchemy import func
from model import (User, Company, Contact, ContactCode, JobCode, ToDoCode,
                   Salary, Job, JobEvent, connect_to_db, db)
from server import app


# Load sample user data to users table
def load_users():
    """Load users from user-example into database."""

    print("Loading users...")

    # Delete all rows in table to make sure there are no duplicates
    User.query.delete()

    # Read user file and insert data
    for row in open("data/user-example.txt"):
        row = row.rstrip()
        fname, lname, email, password = row.split("|")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password)

        # Add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


# load sample contact data to contacts table
def load_contacts():
    """Load contacts from contact-example into database."""

    print("Loading contacts...")

    # Delete all rows in table to make sure there are no duplicates
    Contact.query.delete()

    # Read user file and insert data
    for row in open("data/contact-example.txt"):
        row = row.rstrip()
        contact_id, fname, lname, email, phone, company_id = row.split("|")

        contact = Contact(contact_id=contact_id,
                    fname=fname,
                    lname=lname,
                    email=email,
                    phone=phone,
                    company_id=company_id)

        # Add to the session or it won't ever be stored
        db.session.add(contact)

    # Once we're done, we should commit our work
    db.session.commit()


# load sample company data to companies table
def load_companies():
    """Load companies from company-example into database."""

    print("Loading companies...")

    # Delete all rows in table to make sure there are no duplicates
    Company.query.delete()

    # Read user file and insert data
    for row in open("data/company-example.txt"):
        row = row.rstrip()
        name, street, city, state, zipcode, website = row.split("|")

        company = Company(name=name,
                          street=street,
                          city=city,
                          state=state,
                          zipcode=zipcode,
                          website=website)

        # Add to the session or it won't ever be stored
        db.session.add(company)

    # Once we're done, we should commit our work
    db.session.commit()


# load contact codes (real data!)
def load_contactcodes():
    """Load contact codes from contact-codes.txt into database."""

    print("Loading contact codes...")

    # Delete all rows in table to make sure there are no duplicates
    ContactCode.query.delete()

    # Read user file and insert data
    for row in open("data/contact-codes.txt"):
        row = row.rstrip()
        contact_code, description = row.split("|")

        contactcode = ContactCode(contact_code=contact_code,
                          description=description)

        # Add to the session or it won't ever be stored
        db.session.add(contactcode)

    # Once we're done, we should commit our work
    db.session.commit()


# load job codes (real data!)
def load_jobcodes():
    """Load job codes from job-codes.txt into database."""

    print("Loading job codes...")

    # Delete all rows in table to make sure there are no duplicates
    JobCode.query.delete()

    # Read user file and insert data
    for row in open("data/job-codes.txt"):
        row = row.rstrip()
        job_code, description = row.split("|")

        jobcode = JobCode(job_code=job_code,
                          description=description)

        # Add to the session or it won't ever be stored
        db.session.add(jobcode)

    # Once we're done, we should commit our work
    db.session.commit()


# load to do codes (real data!)
def load_todocodes():
    """Load todo codes from job-codes.txt into database."""

    print("Loading todo codes...")

    # Delete all rows in table to make sure there are no duplicates
    ToDoCode.query.delete()

    # Read file and insert data
    for row in open("data/todo-codes.txt"):
        row = row.rstrip()
        todo_code, description, sugg_due_date = row.split("|")

        todocode = ToDoCode(todo_code=todo_code,
                            description=description,
                            sugg_due_date=sugg_due_date)

        # Add to the session or it won't ever be stored
        db.session.add(todocode)

    # Once we're done, we should commit our work
    db.session.commit()


# load salaries (real data!)
def load_salaries():
    """Load salaries from salaries-data.tsv into database."""

    print("Loading salaries...")

    # Delete all rows in table to make sure there are no dupes
    Salary.query.delete()

    # Read file and insert data
    for row in open("data/salaries-data.tsv"):
        row = row.rstrip()
        metro, job_title, avg_salary, yoy_salary = row.split("\t")

        salary = Salary(metro=metro,
                        job_title=job_title,
                        avg_salary=avg_salary,
                        yoy_salary=yoy_salary)

        # Add to the session
        db.session.add(salary)

    # commit the session to database
    db.session.commit()


# load jobs
def load_jobs():
    """Load fake sample job data from job-example.txt into database"""

    print("Loading jobs...")

    # Delete all rows in table to make sure there are no dupes
    Job.query.delete()

    # Read file and insert data
    for row in open("data/job-example.txt"):
        row = row.rstrip()
        title, link, company_id, active_status, notes = row.split("|")

        job = Job(title=title, link=link, company_id=company_id, active_status=bool(active_status), notes=notes)

        # Add to the session
        db.session.add(job)

    # commit the session to database
    db.session.commit()


# load job events
def load_jobevents():
    """Load fake sample job event data from job-event-example.txt into database"""

    print("Loading job events...")

    # Delete all rows in table to make sure there are no dupes
    JobEvent.query.delete()

    # Read file and insert data
    for row in open("data/job-event-example.txt"):
        row = row.rstrip()
        job_id, user_id, job_code, date_created = row.split("|")

        job_event = JobEvent(job_id=job_id, user_id=user_id, job_code=job_code, date_created=date_created)

        # Add to the session
        db.session.add(job_event)

    # commit the session to database
    db.session.commit()


##############################################################################
# Helper functions
def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data

    load_salaries()
    load_contactcodes()
    load_jobcodes()
    load_todocodes()

    load_users()
    load_companies()
    load_contacts()

    load_jobs()
    load_jobevents()

    set_val_user_id()
