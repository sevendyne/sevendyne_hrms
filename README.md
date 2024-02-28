# sevendyne_hrms

**Install dependencies**

sudo apt update
sudo apt install python3 python3-pip python3-venv git

source venv/bin/activate (on windows use "venv\Scripts\activate)

**Install Django & Libjpeg**

pip install django
sudo apt-get install libjpeg-dev
    
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata states countries

**Create user groups and permissions:**

    ```bash
    python manage.py create_groups_and_permissions
    ```
**Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to set up the superuser account. For example:
    
    - Username: admin
    - Email: [leave blank]
    - Password: admin

    For Windows
    
    ```bash
    python manage.py createsuperuser --username yourusername --email youremail@example.com --noinput - Add username and email address
    ```

**Test Credentials**

Admin: username - admin , password - admin
Client: username - hrmsclient1 , password - password@123, hrmsclient1@example.com 
Employee: username - employee1, password - password@123

