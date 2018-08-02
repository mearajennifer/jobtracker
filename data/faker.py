"""Create fake user, company, and job data from Faker """

from faker import Faker
fake = Faker()


def create_users():
    """Create fake users for job hunt app"""

    with open("data/user-example.txt", "a") as myfile:
        count = 0
        while count < 10:
            fname = fake.first_name()
            lname = fake.last_name()
            email = fake.email()
            password = fake.password()
            myfile.write("{}|{}|{}|{}\n".format(fname, lname, email, password))
            count += 1


def create_companies():
    """Create fake companies for jub hunt app"""

    with open("data/company-example.txt", "a") as myfile:
        count = 0
        while count < 5:
            name = fake.company()
            street = fake.street_address()
            city = fake.city()
            state = fake.state_abbr()
            zipcode = fake.zipcode()
            website = fake.url()
            myfile.write("{}|{}|{}|{}|{}|{}\n".format(name, street, city, state, zipcode, website))
            count += 1


def create_jobs():
    """Create fake jobs for job hunt app"""

    with open("data/job-example.txt", "a") as myfile:
        count = 0
        while count < 6:
            title = fake.job()
            link = fake.url()
            company_id = fake.random_int(min=21, max=25)
            active_status = True
            notes = fake.bs()
            myfile.write("{}|{}|{}|{}|{}\n".format(title, link, company_id, active_status, notes))
            count += 1


def create_job_events():
    """Create fake job events for job hunt app"""

    with open("data/job-event-example.txt", "a") as myfile:
        count = 0
        while count < 6:
            job_id = fake.random_int(min=25, max=30)
            user_id = 5
            job_code = fake.random_int(min=1, max=8)
            date = fake.date_this_year()
            myfile.write("{}|{}|{}|{}\n".format(job_id, user_id, job_code, date))
            count += 1


def create_contacts():
    """Create fake contacts for job hunt app"""

    with open("data/contact-example.txt", "a") as myfile:
        count = 0
        while count < 5:
            fname = fake.first_name()
            lname = fake.last_name()
            company_id = fake.random_int(min=21, max=25)
            myfile.write("{}|{}|{}\n".format(fname, lname, company_id))
            count += 1


def create_contact_events():
    """Create fake contact events for job hunt app"""

    with open("data/contact-event-examples.txt", "a") as myfile:
        count = 0
        while count < 6:
            user_id = 5
            contact_id = fake.random_int(min=21, max=25)
            contact_code = fake.random_int(min=1, max=5)
            date = fake.date_this_year()
            myfile.write("{}|{}|{}|{}\n".format(user_id, contact_id, contact_code, date))
            count += 1
