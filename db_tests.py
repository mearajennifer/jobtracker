"""Tests for the jobs database with real and sample data"""

from model import JobCode, JobEvent, Job, ToDo, ToDoCode, db
from datetime import datetime
from datetime import timedelta


# test adding a job
def add_job_return_event_desc():
    """Adds a new job to the database for a user"""

    # create job and add to database jobs table
    job = Job(title="Software Engineer", company_id=1, active_status=True)
    db.session.add(job)
    db.session.commit()

    # create job event for new job and add to database table
    jobevent = JobEvent(user_id=1, job_id=job.job_id, job_code=1, date_created=datetime.now())
    db.session.add(job)
    db.session.commit()

    # query for job event description
    event_desc = JobCode.query.filter(JobCode.job_code == jobevent.job_code).one()

    return event_desc.description


def trigger_to_do_from_job_event():
    """Adds a new todo for the job"""

    # create job and add to database table
    job = Job(title="Software Engineer", company_id=1, active_status=True)
    db.session.add(job)
    db.session.commit()

    # create job event for new job and add to database table
    jobevent = JobEvent(user_id=1, job_id=job.job_id, job_code=1, date_created=datetime.now())
    db.session.add(jobevent)
    db.session.commit()

    # create dates
    date_created = datetime.now()
    date_due = date_created + timedelta(days=7)

    # create todo and add to database table
    todo = ToDo(job_event_id=jobevent.job_event_id, todo_code=4, date_created=date_created, date_due=date_due)
    db.session.add(todo)
    db.session.commit()

    event_desc = JobCode.query.filter(JobCode.job_code == jobevent.job_code).one()
    todo_desc = ToDoCode.query.filter(ToDoCode.todo_code == todo.todo_code).one()

    return f"To Do: ({todo_desc.description}) triggered for ({event_desc.description}) job event for user ({User.query.get(jobevent.user_id).fname})"


def add_salary_to_job():
    """Looks up salary in salaries and adds to job"""

    # create job and add to database table
    job = Job(title="Software Engineer", company_id=1, active_status=True)
    db.session.add(job)
    db.session.commit()

    salary = Salary.query.filter(metro="San Francisco", job_title="Software Engineer").avg_salary.one()
    avg_salary = salary.avg_salary

    job.avg_salary = avg_salary
    db.session.commit()

    return f"The average salary for {job.title} in {salary.metro} is {job.avg_salary}"
