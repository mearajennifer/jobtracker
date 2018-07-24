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
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<user user_id={self.user_id} name={self.fname} {self.lname}>"


class Contact(db.Model):
    """A user's contact."""

    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<contact contact_id={self.contact_id} name={self.fname} {self.lname}>"


class ContactTracking(db.Model):
    """Track user and contact interactions."""

    __tablename__ = 'contact_tracking'

    contact_track_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    contact_id - db.Column(db.Integer, db.ForeignKey('contacts.contact_id'), nullable=False)
    code = db.Column(db.Integer, db.ForeignKey('contact_codes.code'))
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<tracking user_id={self.user_id} contact_id={self.contact_id} date={self.date}>"


class ContactCode(db.Model):
    """Codes corresponding to various user interactions with contacts."""

    __tablename__ = 'contact_codes'

    code = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<contact code={self.code} desc={self.description}>"


class ContactToDo(db.Model):
    """To dos for a specific contact connected to the user."""

    __tablename__ = 'contact_todos'

    contact_todo_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    contact_track_id = db.Column(db.Integer, db.ForeignKey('contact_tracking.contact_track_id'), nullable=False)
    code = db.Column(db.Integer, db.ForeignKey('to_do_codes.code'), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    date_due = db.Column(db.Date, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<contact to-do id={self.contact_todo_id} to-do code={self.code}>"


class ToDoCode(db.Model):
    """Codes corresponding to various user to-do items."""

    __tablename__ = 'to_do_codes'

    code = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<to-do code={self.code} desc={self.description}>"


class Company(db.Model):
    """Company that has a job listings or contacts."""

    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<company company_id={self.company_id} name={self.name}>"


class Job(db.Model):
    """Job listing at a company that a user is tracking."""

    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    avg_salary = db.Column(db.String(11), db.nullable=True)
    active_status = db.Column(db.Boolean, nullable=False)









































