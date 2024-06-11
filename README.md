# sevendyne_hrms

**Install dependencies**

- sudo apt update
- sudo apt install python3 python3-pip python3-venv git
- source venv/bin/activate (on Windows use "venv\Scripts\activate")
- pip install django
- sudo apt-get install libjpeg-dev
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py loaddata states countries

**Celery Configuration in bin/activate:**

- cd ~/sevendyne_hrms/venv/bin/
- nano activate
- ...
export DJANGO_SETTINGS_MODULE=sevendyne_hrms.settings  # Add this line
...

**Postgres Database Configuration**

- sudo su postgres
- createdb sevendyne_hrms
- createuser -P sevendyne
- role - sevendyne
- password for role - sevendyne@123
- psql
- grant all privileges on database sevendyne_hrms to sevendyne;
- \q
- exit


**Create user groups and permissions:**

- python manage.py create_groups_and_permissions

**Create a superuser:**

- python manage.py createsuperuser

Follow the prompts to set up the superuser account. For example:
- Username: admin
- Email: [leave blank]
- Password: admin

For Windows

- python manage.py createsuperuser --username yourusername --email youremail@example.com --noinput - Add username and email address

**Test Credentials**

- Admin: username - admin , password - admin
- Client: username - hrmsclient1 , password - password@123, hrmsclient1@example.com 
- Employee: username - employee1, password - password@123

**Run the app**: python manage.py runserver 0.0.0.0:8000
- Open your browser and type localhost:8000 and you will see the app running. Cheers!!!


**To Backup the database**

- python manage.py dbbackup
