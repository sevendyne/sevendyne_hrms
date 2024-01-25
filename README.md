# sevendyne_hrms

1. virtualenv venv
2. source venv/bin/activate (on windows use "venv\Scripts\activate)
3. pip install -r requirements.txt
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py loaddata states countries
8.Create user groups and permissions:

    ```bash
    python manage.py create_groups_and_permissions
    ```

9. Create a superuser:

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
10. sevendyne admin --- username - admin , password - admin
11. hrms client --- username - hrmsclient1 , password - password@123 , hrmsclient1@example.com 

