# Movies

Small Exams service to create and share exams sheets, solve tasks and receive final grades.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* Python >= 3.6.5 <br />
* Django >= 2.2 <br />
* PostgreSQL >= 9.5 <br />


### Environment:
Before you run the project you need to create a **.env** file.
* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django app Secret Key
* DB_NAME - database name
* DB_USER - database user name
* DB_PASSWORD - databas password

### Installing
##### With Makefile
You can create virtual environment _(you need virtualenv installed)_, install dependencies, migrate,
 apply fixtures and runserver with 1 command:
```
make install
```
**Fixtures:** <br />
If you apply fixtures - you will have 2 users created:
- **first_user** pass: **test12345**
- **second_user** pass: **test12345**
##### Manually
To use minimal basic requirements version run:
```
pip install -r requirements/base.txt
```

To use full development version run:
```
pip install -r requirements.txt
```

### Available API
**User registration:**
```
rest-auth/registration/
rest-auth/login/
rest-auth/logout/
```
**Exams:**
```
/api/exams/
/api/exams_sheets/
/api/tasks_sheets/
/api/api/tasks//
/api/marks_range/
```
**Users:**
```.env
/core/users/
```
### Running the tests
You can run tests using [pytest](https://docs.pytest.org/en/latest/): 
```
pytest
```
or
```
make test
```
### And coding style tests

Test style adjustments accordingly to PEP8:

```
flake8 .
```

### Security tests

Small check against the most popular vulnerabilities with [bandit](https://bandit.readthedocs.io/en/latest/) tool.

```
bandit -r .
```

### HOWTO:
**Description:**<br />
API module for creating Exams service.
Provides possibilities:
- create Exam Sheets (collection of Task Sheets), edit and delete for its creator and view for another users
- create Task Sheets - question, accepted answer and score
- create Exam - for user who want to pass selected Exam Sheet
- create Task - user provides his answer for selected Task Sheet

Also optionally Exam Sheet creator can assign Marks Range - and this allows to show final grade for the user depending
on his answers.

**A typical workflow looks like this:**
1. Register a new user and login <br />
2. Create exam template:<br />
2-0 (OPTIONALLY) Create a new **Marks Range** <br />
2-1. Create a new **Exam Sheet**<br />
3. Create several new **Task Sheet**s for this Exam Sheet.
4. If you want to solve an exam - create an **Exam** and select available Exam Sheets.
5. To solve the Exam - you should create a **Task** for each TaskSheet assigned to selected Exam, write your answer and save.
 Repeat with all available TaskSheets and you will get a final grade at the end.


## Built With

* [Django](https://docs.djangoproject.com/en/2.2/) - The web framework used
* [Django Rest Framework](https://www.django-rest-framework.org/) - Framework for API building
* [DRY Rest Permissions](https://github.com/dbkaplan/dry-rest-permissions) - Permissions
* [Django REST Auth](https://django-rest-auth.readthedocs.io/en/latest/) - Authentication via DRF



## Author

* **Chiefir** - [LinkedIn](https://www.linkedin.com/in/andrii-isiuk/)
