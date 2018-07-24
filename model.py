"""Model and database function for job hunt app project."""

from flask_sqlalchemy import SQLAlchemy

# Connect to the PostgreSQL database
db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User of job hunt app."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User id={self.user_id} name={self.fname} {self.lname}>"


class Contact(db.Model):
    """A user's contact."""

    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    companies = db.relationship('Company', backref=db.backref('contacts', order_by=contact_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Contact id={self.contact_id} name={self.fname} {self.lname}>"


class ContactEvent(db.Model):
    """Track user and contact events outside of a job, such as networking or informational interviews."""

    __tablename__ = 'contact_events'

    contact_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'), nullable=False)
    contact_code = db.Column(db.Integer, db.ForeignKey('contact_codes.contact_code'))
    date_created = db.Column(db.Date, nullable=False)

    users = db.relationship('User', backref=db.backref('contact_events', order_by=contact_event_id))
    contacts = db.relationship('Contact', backref=db.backref('contact_events', order_by=contact_event_id))
    contact_codes = db.relationship('ContactCode', backref=db.backref('contact_events', order_by=contact_event_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<ContactEvent user_id={self.user_id} contact_id={self.contact_id} date={self.date_created}>"


class ContactCode(db.Model):
    """Codes corresponding to various user events with contacts."""

    __tablename__ = 'contact_codes'

    contact_code = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<ContactCode code={self.contact_code} desc={self.description}>"


class Company(db.Model):
    """Company that has a job listings or contacts."""

    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Company id={self.company_id} name={self.name}>"


class Job(db.Model):
    """Job listing at a company that a user is tracking."""

    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    avg_salary = db.Column(db.String(15), nullable=True)
    active_status = db.Column(db.Boolean, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    companies = db.relationship('Company', backref=db.backref('jobs', order_by=job_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Job job_id={self.job_id} title={self.title} company={self.companies.name}>"


class JobEvent(db.Model):
    """Track events in status of job application."""

    __tablename__ = 'job_events'

    job_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=False)
    job_code = db.Column(db.Integer, db.ForeignKey('job_codes.job_code'), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    users = db.relationship('User', backref=db.backref('job_events', order_by=job_event_id))
    jobs = db.relationship('Job', backref=db.backref('job_events', order_by=job_event_id))
    job_codes = db.relationship('JobCode', backref=db.backref('job_events', order_by=job_event_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<JobEvent id={self.job_event_id} event={self.job_codes.description}>"


class JobCode(db.Model):
    """Codes corresponding to various user events with jobs."""

    __tablename__ = 'job_codes'

    job_code = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<JobCode code={self.job_code} desc={self.description}>"


class ToDo(db.Model):
    """Creates todos based on job events or contact events."""

    __tablename__ = 'todos'

    todo_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    job_event_id = db.Column(db.Integer, db.ForeignKey('job_events.job_event_id'), nullable=True)
    contact_event_id = db.Column(db.Integer, db.ForeignKey('contact_events.contact_event_id'), nullable=True)
    todo_code = db.Column(db.Integer, db.ForeignKey('todo_codes.todo_code'), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    date_due = db.Column(db.Date, nullable=False)

    job_events = db.relationship('JobEvent', backref=db.backref('todos', order_by=todo_id))
    contact_events = db.relationship('ContactEvent', backref=db.backref('todos', order_by=todo_id))
    todo_codes = db.relationship('ToDoCode', backref=db.backref('todos', order_by=todo_id))

    def __repr__(self):
        """Proved helpful representation when printed."""

        return f"<ToDo id={self.todo_id} todo-desc={self.todo_codes.description}>"


class ToDoCode(db.Model):
    """Codes corresponding to various user todo items."""

    __tablename__ = 'todo_codes'

    todo_code = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    sugg_due_date = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<ToDoCode code={self.todo_code} desc={self.description}>"


class Salary(db.Model):
    """Average salary for common job titles in metro areas of the United States."""

    __tablename__ = 'salaries'

    salary_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    metro = db.Column(db.String(20), nullable=False)
    job_title = db.Column(db.String(40), nullable=False)
    avg_salary = db.Column(db.String(15), nullable=False)
    yoy_salary = db.Column(db.String(7), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Salary job={self.job_title} metro={self.metro} salary={self.avg_salary}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
