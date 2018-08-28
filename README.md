# ![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/JobTracker-nobg2.png "JobTracker")
The job search can be overwhelming. JobTracker helps the overwhelmed job seeker track jobs they’ve applied to, companies they are interested in, or networking contacts they have met. It uses a complex PostgresQL database to store user added data and is built with a Python/Flask backend.

## About Me
Before studying at Hackbright Academy, Jennifer worked for 10+ years in marketing and project management. She started as a studio coordinator directing creative teams and impacting operational efficiency. Next she managed multi-faceted marketing campaigns and social media channels for Kaiser Permanente. This work allowed her to engage in the technical details of building websites, deploying applications, and training users. She found a love for coding and decided to embark on a new path in software engineering. She enjoys programming because it allows her to solve complex problems, design and build solutions, and continue learning new technical concepts and languages.

## Deployment
http://yourjobtracker.com/

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future State](#future)
* [Installation](#installation)
* [License](#license)

## <a name="tech-stack"></a>Technologies
* Python
* Flask
* Jinja2
* PostgresQL
* SQLAlchemy ORM
* HTML
* CSS
* Bootstrap
* React
* jQuery
* Google Calendar

## <a name="features"></a>Features

#### Landing Page
Users register or login on the React JS built landing page.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/landing-page.gif "JobTracker landing page")

#### Active Jobs Dashboard
Once signed in, they view the first major aspect of the app, the active jobs dashboard, built with Jinja2 templating and using SQLAlchemy ORM database queries. Here users can sort jobs by columns using JavaScript, view the most recent status of a job, archive associated tasks, or add tasks to their Google Calendar using the Google OAuth 2 authentication and Calendar API. As the hiring process continues, users can update the status of a job application, and will be assigned new follow up tasks and due dates. 

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/active-jobs.png "JobTracker active jobs dashboard")

#### Add A Job
Users can add new jobs, and select an existing company or create a new one, plus add necessary details.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/add-a-job.png "JobTracker add a job modal")

#### Job Information
Individual job pages offer more tracking information and a history of status updates and tasks. Using the latest job salary data from Glassdoor Research, users can select their metro area and job title, and the job information is updated with an average salary via JavaScript AJAX post request.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/job-info-salary.gif "JobTracker job information page")

#### Company Information
Users also get an overview of a company and its associated jobs and contacts and can edit important information also with an AJAX request.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/company-page.png "JobTracker company information page")

#### Archived Jobs Dashboard
The archived jobs page shows all jobs where users have not gotten a job offer, or accepted or declined an offer.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/archived-jobs.png "JobTracker archived jobs dashboard")

#### Companies Dashboard
The companies page displays each one and how many jobs they’ve applied to there, also with column sorting.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/companies.png "JobTracker companies dashboard")

#### Contacts Dashboard
And similarly with the contacts page, you see all contacts, most recent interactions, and follow up tasks.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/contacts.png "JobTracker contacts dashboard")

#### Add A Contact
New contacts can also be added to existing or new companies. And contact pages show more detailed information about contacts. 

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/add-a-contact.png "JobTracker add a contact modal")

#### User Profile
The user profile page is also built in React and details the user’s analytics from number of jobs interested in to the number of job offers received. It also gives user’s an inspirational quote randomizer built in Javascript, to help them on days when they need motivation.

![alt text](https://github.com/mearajennifer/jobtracker/blob/master/static/img/user-profile-motivation.gif "JobTracker user profile")

## <a name="future"></a>Future State
The project roadmap for JobTracker has several features planned out for the next sprint:
* Job and company ranking system
* Full calendar functionality where users can track tasks, but also job interviews and networking events
* Password hashing
* Customized tasks and due dates

## <a name="installation"></a>Installation
To run JobTracker on your own machine:

Install PostgresQL (Mac OSX)

Clone or fork this repo:
```
https://github.com/mearajennifer/jobtracker.git
```

Create and activate a virtual environment inside your JobTracker directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Google Calendar API](https://developers.google.com/calendar/)

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export GOOGLE_API_KEY="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_ID_HERE"
```

Set up and download your Google OAuth 2.0 client IDs, and save to a file called <kbd>client_secrets.json</kbd>.

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb jobs
python3.6 model.py
python3.6 seed.py
```

Run the app:

```
python3.6 server.py
```

You can now navigate to 'localhost:5000/' to access JobTracker.

## <a name="license"></a>License
The MIT License (MIT) Copyright (c) 2016 Agne Klimaite

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
