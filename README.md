# JobTracker
The job search can be overwhelming. JobTracker helps the overwhelmed job seeker track jobs they’ve applied to, companies they are interested in, or networking contacts they have met. It uses a complex PostgresQL database to store user added data and is built with a Python/Flask backend.

## Deployment
http://yourjobtracker.com/

## Contents
* Tech Stack
* Features
* Future State
* Installation
* About Me

## Technologies
Backend: Python, Flask, Jinja, PostgreQL, SQLAlchemy ORM, 
Frontend: HTML, CSS, Bootstrap, React, jQuery
APIs: Google Calendar

## Features

#### Landing Page
Users register or login on the React JS built landing page.
gif of landing page/registration page

#### Active Jobs Dashboard
Once signed in, they view the first major aspect of the app, the active jobs dashboard, built with Jinja2 templating and using SQLAlchemy ORM database queries. Here users can sort jobs by columns using JavaScript, view the most recent status of a job, archive associated tasks, or add tasks to their Google Calendar using the Google OAuth 2 authentication and Calendar API. As the hiring process continues, users can update the status of a job application, and will be assigned new follow up tasks and due dates. 
image of active jobs dashboard

#### Add A Job
Users can add new jobs, and select an existing company or create a new one, plus add necessary details.
image of new job modal

#### Job Information
Individual job pages offer more tracking information and a history of status updates and tasks. Using the latest job salary data from Glassdoor Research, users can select their metro area and job title, and the job information is updated with an average salary via JavaScript AJAX post request.
gif of adding job salary

#### Company Information
Users also get an overview of a company and its associated jobs and contacts and can edit important information also with an AJAX request.

#### Archived Jobs Dashboard
The archived jobs page shows all jobs where users have not gotten a job offer, or accepted or declined an offer.

#### Companies Dashboard
The companies page displays each one and how many jobs they’ve applied to there, also with column sorting.

#### Contacts Dashboard
And similarly with the contacts page, you see all contacts, most recent interactions, and follow up tasks.

#### Add A Contact
New contacts can also be added to existing or new companies. And contact pages show more detailed information about contacts. 

#### User Profile
The user profile page is also built in React and details the user’s analytics from number of jobs interested in to the number of job offers received. It also gives user’s an inspirational quote randomizer built in Javascript, to help them on days when they need motivation.

## Future State

## Installation

## About Me


## License
The MIT License (MIT) Copyright (c) 2016 Agne Klimaite

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
