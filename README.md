# spatialTrainingPlatform
SIIP Project
# Project Title

A scalable online platform for Evaluation and Training Visuospatial Skills
## Path to Templates of Surveys
django_project > templates
## Surveys
Survey: game habits;
Survey2: gaming motivations, 44 questions;
Survey3: question that redirects to two different pages (choose yes to continute to survey4,choose no to the end of the survey);
Survey4: Emotional Experiences in Games Questionnaire;
Survey5: Age, gender, ethnicity

## Unfinished tasks checklist:
survey3 redirect,test answer log in database, intropage and nav bar, result page(summary)

## Deploy on Local Host

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 2.7
MySQL
```

### Installing

Start mySQL service and Create a mySQL database named "platform_demo"

```
mysql.server start
mysql -u root -p
create database platform_demo;
```
Install Dependencies (under the directory)
```
pip install -r requirements.txt
pip install mysql-python
```
### Start Server

Prepare the database
```
python manage.py syncdb
python manage.py migrate
```
import test answer
```
import SIIPproject_testanswer.csv to SIIPproject_testanswer table
note: try to use MySQLWorkBench in this step.
```
Start the server
```
python manage.py runserver
```
